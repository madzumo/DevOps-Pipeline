import boto3
import os
import time

class AWSconfig:
    def __init__(self, key_id='', secret_id='', region = "us-east-1", instance_type = "t3.large"):
        self.key_id = key_id
        self.secret_id = secret_id
        self.region = region
        self.instance_type = instance_type
        self.instance_ID = ''
        self.tag_key = 'madzumo'
        self.tag_value = 'demo'
        self.instance_ami = 'ami-0c101f26f147fa7fd'
        self.key_pair_name = 'madzumo-key-pair'
        if key_id != '':
            os.environ['AWS_ACCESS_KEY_ID'] = self.key_id
        if secret_id != '':
            os.environ['AWS_SECRET_ACCESS_KEY'] = self.secret_id
        os.environ['AWS_DEFAULT_REGION'] = self.region
        
        
    def view_s3_buckets():
        s3 = boto3.resource('s3')
        for bucket in s3.buckets.all():
            print(bucket.name)
    
    def get_vpc():
        vpc = boto3.resource('ec2')
        response = vpc.describe_vpcs
        print(response)
        
    def create_ec2_instance(self):
        ec2 = boto3.client('ec2')
        #get default vpc id
        response = ec2.describe_vpcs(
            Filters=[
                {
                    'Name': 'is-default', 
                    'Values': ['true']
                }
            ]
        )
    
        default_vpc_id = response['Vpcs'][0]['VpcId']
        
        #check to make sure sg is not present
        response = self._get_security_group()
        if response['SecurityGroups']:
            print("Security Group present")
        else:
            #create new security group
            sg_madzumo = ec2.create_security_group(
                GroupName = 'madzumo-sg',
                Description = 'madzumo sg - ssh http https',
                VpcId = default_vpc_id,
                TagSpecifications= [
                        {
                            'ResourceType': 'security-group',
                            'Tags': [
                                {
                                    'Key': 'Name',
                                    'Value': 'madzumo-sg'
                                },
                                {
                                    'Key': 'madzumo',
                                    'Value': 'demo'
                                }
                            ]
                        }
                    ]
            )

            ec2.authorize_security_group_ingress(
                GroupId = sg_madzumo['GroupId'],
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 22,
                        'ToPort': 22,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    },
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 80, 
                        'ToPort':   80,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    }
                ]
            )
            
            ec2.authorize_security_group_egress(
                GroupId = sg_madzumo['GroupId'],
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 0,
                        'ToPort': 0,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    }
                ]
            )
            print("Created Security Group")
            
            
        response = self._get_key_pair()
        if response['KeyPairs']:
            print ("Key Pair present")
        else:
            try:
                # Create a new key pair
                response = ec2.create_key_pair(KeyName = self.key_pair_name)
                key_material = response['KeyMaterial']
                with open(self.key_pair_name, 'w') as file:
                    file.write(key_material)
                print("Key Pair created")
            except Exception as ex:
                print(f"Error creating key pair:\n{ex}")
                return

        response = self._get_ec2_instance()
        if response['Reservations']:
            print ("EC2 instance present")
        else:
            try:
                # Launch a new EC2 instance
                ec2 = boto3.resource('ec2')
                instance = ec2.create_instances(
                    ImageId = self.instance_ami,
                    MinCount = 1,
                    MaxCount = 1,
                    InstanceType = self.instance_type,
                    KeyName = self.key_pair_name,
                    SecurityGroups=['madzumo-sg'],
                    TagSpecifications= [
                        {
                            'ResourceType': 'instance',
                            'Tags': [
                                {
                                    'Key': 'Name',
                                    'Value': 'madzumo-jenkins'
                                },
                                {
                                    'Key': 'madzumo',
                                    'Value': 'demo'
                                }
                            ]
                        }
                    ]
                )[0]
                self.instance_ID = instance.id
                print("Instance ID:", instance.id)
            except Exception as ex:
                print(f"Error creating Instance:\n{ex}")
                return
            
    def delete_ec2_instance(self):
        ec2_resource = boto3.resource('ec2')

        response = self._get_ec2_instance()
        # if it exists then delete it
        if response['Reservations']:
            for reservation in response['Reservations']:
                for instancex in reservation['Instances']:
                    you_are_terminated = ec2_resource.Instance(instancex['InstanceId'])
                    response = you_are_terminated.terminate()
                    print(f"EC2 instance {instancex['InstanceId']} terminated.\n Waiting for completion...")
                    time.sleep(10)
        else:
            print("No Ec2 Instance found for this demo")

        response = self._get_security_group()
        # if it exists then delete it
        if response['SecurityGroups']:
            for groupie in response['SecurityGroups']:
                you_are_terminated = ec2_resource.SecurityGroup(groupie['GroupId'])
                response = you_are_terminated.delete()
                print(f"Security Group {groupie['GroupId']} terminated.")
        else:
            print("No Security Group found for this demo")
         
        # delete madzumo key pair
        response = self._get_key_pair()
        if response['KeyPairs']:
            you_are_terminated = ec2_resource.KeyPair(self.key_pair_name)
            response = you_are_terminated.delete()
            print(f"Key Pair {response['KeyPairId']} terminated.")
        else:
            print("No Key Pair for this demo")
    
    def _get_ec2_instance(self):
        # Find the madzumo ec2 instance
        ec2 = boto3.client('ec2')
        response = ec2.describe_instances(
            Filters = [
                {
                        'Name': 'tag:madzumo',
                        'Values': ['demo']
                }
            ]
        )
        return response
    
    def _get_security_group(self):
        # Find the madzumo security group
        ec2 = boto3.client('ec2')
        response = ec2.describe_security_groups(
            Filters = [
                {
                    'Name': 'tag:madzumo',
                    'Values': ['demo']
                }
            ]
        )
        return response
    
    def _get_key_pair(self):
        # find if security key pair exists
        ec2 = boto3.client('ec2')
        response = ec2.describe_key_pairs(
            Filters = [
                {
                    'Name': 'key-name',
                    'Values': [self.key_pair_name]
                }
            ]
        )
        return response
 
 #******************************************************************************   
    def _wait_for_instance_2_load():
        while True:
            # new_response = ec2_client.describe_instances(InstanceIds=[target_instance])
            # instance_status = new_response['Reservations'][0]['Instances'][0]['State']['Name']
            time.sleep(10)
            new_response = ec2_client.describe_instance_status(InstanceIds=[instance_id])
            instance_state = new_response['InstanceStatuses'][0]['InstanceState']['Name']
            instance_status = new_response['InstanceStatuses'][0]['InstanceStatus']['Details'][0]['Status']
            print(f"{get_current_time()} - EC2 instance {instance_id}: {instance_state} & {instance_status}")

            if instance_state == 'running' and instance_status == 'passed':
                break
            
    def _get_current_time():
        eastern = pytz.timezone('US/Eastern')
        current_time = datetime.now(eastern)
        military_time = current_time.strftime('%H:%M:%S')
        return military_time
    
    def _wait_for_instance_2_die():
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                # print(instance_id)
        new_response = ec2_client.describe_instance_status(InstanceIds=[instance_id])
        instance_state = new_response['InstanceStatuses'][0]['InstanceState']['Name']
        if instance_state == 'terminated':
            create_ec2_instance()
        elif instance_state == 'running':
            get_instance_host_ip_info()
            print(f"EC2 instance RUNNING with ID: {instance_id}")
        else:
            print(f"Unknown state of existing instance: {instance_state}")
            sys.exit()