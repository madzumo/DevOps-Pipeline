import python.aws_madzumo as aws_madzumo
import python.helper as helper
import boto3
import os
from time import sleep

class Ec2Config(aws_madzumo.AWSbase):
    def __init__(self, key_id='', secret_id='', region="us-east-1", instance_name = ''):
        super().__init__(key_id, secret_id, region)
        self.ec2_client = boto3.client('ec2')
        self.ec2_resource = boto3.resource('ec2')
        self.ec2_instance_name = instance_name
        self.ec2_instance_public_ip = ''
        self.ec2_instance_id = ''
        self.ec2_instance_private_ip = ''
        self.ec2_instance_public_dnsname = ''
        self.ec2_instance_subnet_id = ''
        self.ec2_instance_vpc_id = ''
        
    def create_ec2_instance(self, instance_name):
        """Creates Instance in Default VPC. Instance Name required."""
        self.ec2_instance_name = instance_name
        
        if self.get_instance():
            print ("EC2 instance already present")
            self.populate_ec2_instance(self.ec2_instance_name)
        else:
            self.create_security_group() 
            self.create_key_pair()
            try: # Launch a new EC2 instance
                resultx = self.ec2_resource.create_instances(
                    ImageId = self.instance_ami,
                    MinCount = 1,
                    MaxCount = 1,
                    InstanceType = self.instance_type,
                    KeyName = f"{self.ec2_instance_name}-keypair",
                    SecurityGroups=[f"{self.ec2_instance_name}-sg"],
                    #SubnetId = self.ec2_subnet_id,
                    TagSpecifications= [
                        {
                            'ResourceType': 'instance',
                            'Tags': [
                                {
                                    'Key': 'Name',
                                    'Value': self.ec2_instance_name
                                },
                                {
                                    'Key': self.tag_identity_key,
                                    'Value': self.tag_identity_value
                                }
                            ]
                        }
                    ]
                )[0].id
                print(f"EC2 Instance Created: {resultx}")
                self.ec2_instance_id = resultx
            except Exception as ex:
                print(f"Error creating Instance:\n{ex}")
                return
            
            self.wait_for_instance_to_load()
            self.populate_ec2_instance(self.ec2_instance_name)
            print(f"EC2 Instance Ready. IP: {self.ec2_instance_public_ip}")
            
    def populate_ec2_instance(self, instance_name):
        """Assign ec2 instnace to this object"""
        self.ec2_instance_name = instance_name
        response = self.get_instance()
        if response:
            if response[0]['Instances'][0]['State']['Name'] != 'running':
                print(f"Error: Instance in {response[0]['Instances'][0]['State']['Name']} state")
            else:
                self.ec2_instance_id = response[0]['Instances'][0]['InstanceId']
                self.ec2_instance_public_ip = response[0]['Instances'][0]['PublicIpAddress']
                self.ec2_instance_private_ip = response[0]['Instances'][0]['PrivateIpAddress']
                self.ec2_instance_public_dnsname = response[0]['Instances'][0]['PublicDnsName']
                self.ec2_instance_subnet_id = response[0]['Instances'][0]['SubnetId']
                self.ec2_instance_vpc_id = response[0]['Instances'][0]['VpcId']
        else:
            print(f"Unable to locate instance: {self.ec2_instance_name}")
        
        
    def delete_all_ec2_instances_tag(self):
        response = self.get_all_instances_tag()
        if response:
            for reservation in response['Reservations']:
                for instancex in reservation['Instances']:
                    you_are_terminated = self.ec2_resource.Instance(instancex['InstanceId'])
                    response = you_are_terminated.terminate()
                    print(f"EC2 instance {instancex['InstanceId']} terminated.\n Waiting for completion...")
                    # time.sleep(10)
        else:
            print(f"No Instance found for Tag-> {self.tag_identity_key}:{self.tag_identity_value}")
    
    def delete_ec2_instance(self):
        if self.ec2_instance_id == '':
            "Error: EC2 instance id needed"
        else:
            you_are_terminated = self.ec2_resource.Instance(self.ec2_instance_id)
            you_are_terminated.terminate()
            print(f"EC2 instance {self.ec2_instance_id} terminated.\n Waiting for completion...")
            sleep(10)
            
            self.delete_security_group()
            self.delete_key_pair()
    
    def get_security_group_id (self):
        response = self.ec2_client.describe_security_groups(
            Filters = [
                {
                    'Name': 'tag:Name',
                    'Values': [f"{self.ec2_instance_name}-sg"]
                }
            ]
        )
        if response['SecurityGroups']:
            return response['SecurityGroups'][0]['GroupId']
        else:
            return

    def get_all_security_group_tag(self):
        response = self.ec2_clientec2.describe_security_groups(
            Filters = [
                {
                    'Name': f'tag:{self.tag_identity_key}',
                    'Values': [self.tag_identity_value]
                }
            ]
        )
        return response
     
    def delete_security_group(self):
        this_sg_id = self.get_security_group_id()
        you_are_terminated = self.ec2_resource.SecurityGroup(this_sg_id)
        you_are_terminated.delete()
        print(f"Security Group {this_sg_id} terminated.")
    
    def create_security_group(self):
        if self.get_security_group_id():
            print("Security Group present")
        else:
            sg_madzumo = self.ec2_client.create_security_group(
                GroupName = f"{self.ec2_instance_name}-sg",
                Description = 'ssh http https',
                VpcId =  self.get_default_vpc_id(),
                TagSpecifications= [
                        {
                            'ResourceType': 'security-group',
                            'Tags': [
                                {
                                    'Key': 'Name',
                                    'Value': f"{self.ec2_instance_name}-sg"
                                },
                                {
                                    'Key': self.tag_identity_key,
                                    'Value': self.tag_identity_value
                                }
                            ]
                        }
                    ]
            )

            self.ec2_client.authorize_security_group_ingress(
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
            
            self.ec2_client.authorize_security_group_egress(
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
            print(f"Created Security Group: {self.ec2_instance_name}-sg")
    
    def get_key_pair_id(self):
        response = self.ec2_client.describe_key_pairs(
            Filters = [
                {
                    'Name': 'key-name',
                    'Values': [f"{self.ec2_instance_name}-keypair"]
                }
            ]
        )
        if response['KeyPairs']:
            return response['KeyPairs'][0]['KeyPairId']
        else:
            return
    
    def delete_key_pair(self):
        response = self.get_key_pair_id()
        if response['KeyPairs']:
            you_are_terminated = self.ec2_resource.KeyPair(f"{self.ec2_instance_name}-keypair")
            response = you_are_terminated.delete()
            print(f"Key Pair {response['KeyPairId']} terminated.")
        else:
            print("No Key Pair found")
            
    def create_key_pair(self):
        if self.get_key_pair_id():
            print("Key Pair Present")
        else:
            try:
                response = self.ec2_client.create_key_pair(KeyName = f"{self.ec2_instance_name}-keypair")
                key_material = response['KeyMaterial']
                with open(f"{self.ec2_instance_name}-keypair", 'w') as file:
                    file.write(key_material)
                file_path = f"{os.getcwd()}/{self.ec2_instance_name}-keypair"
                os.chmod(file_path, 0o600)
                print(f"Created Key Pair: {self.ec2_instance_name}-keypair")
            except Exception as ex:
                print(f"Error creating key pair:\n{ex}")
            
    def get_instance(self):
        response = self.ec2_client.describe_instances(
            Filters = [
                {
                    'Name': 'tag:Name',
                    'Values': [self.ec2_instance_name]
                },
                {
                    'Name': 'instance-state-name',
                    'Values': ['running']
                }
            ]
        )
        return response['Reservations']

    def get_instance_id(self):
        response = self.ec2_client.describe_instances(
            Filters = [
                {
                        'Name': 'tag:Name',
                        'Values': [self.ec2_instance_name]
                }
            ]
        )
        if response['Reservations']:
            return response['Reservations'][0]['Instances'][0]['InstanceId']
        else:
            return
    
    def get_all_instances_tag (self):
        response = self.ec2_client.describe_instances(
            Filters = [
                {
                        'Name': f'tag:{self.tag_key_identity}',
                        'Values': [self.tag_value_identity]
                }
            ]
        )
        return response
    
    def get_default_vpc_id(self):
        response = self.ec2_client.describe_vpcs(
            Filters=[
                {
                    'Name': 'is-default', 
                    'Values': ['true']
                }
            ]
        )
        return response['Vpcs'][0]['VpcId']
    
    def wait_for_instance_to_load(self):
        """Waits until Instance State = running and Instance Status = passed. Have Instance ID assigned."""
        while True:
            print (f"{helper._get_current_time()} Waiting for instance to initialize.....")
            sleep(20)
            new_response = self.ec2_client.describe_instance_status(InstanceIds=[self.ec2_instance_id])
            if new_response['InstanceStatuses']:
                instance_state = new_response['InstanceStatuses'][0]['InstanceState']['Name']
                instance_status = new_response['InstanceStatuses'][0]['InstanceStatus']['Details'][0]['Status']
                # print(f"{helper._get_current_time} - EC2 instance {self.ec2_instance_name}: {instance_state} & {instance_status}")

                if instance_state == 'running' and instance_status == 'passed':
                    break
                
            