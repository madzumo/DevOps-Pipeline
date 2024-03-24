import boto3

# Clients
ec2_client = boto3.client('ec2')
eks_client = boto3.client('eks')

# Step 1: Create a VPC
vpc_response = ec2_client.create_vpc(CidrBlock='10.0.0.0/16')
vpc_id = vpc_response['Vpc']['VpcId']
print(f"VPC Created: {vpc_id}")

# Get a list of all availability zones in the region
azs_response = ec2_client.describe_availability_zones()
availability_zones = [az['ZoneName'] for az in azs_response['AvailabilityZones']][:4]  # Limit to 4 AZs

# Step 2: Create 4 Subnets in different Availability Zones
subnet_ids = []
for i, az in enumerate(availability_zones, start=1):
    subnet_response = ec2_client.create_subnet(
        CidrBlock=f'10.0.{i}.0/24',
        VpcId=vpc_id,
        AvailabilityZone=az
    )
    subnet_id = subnet_response['Subnet']['SubnetId']
    subnet_ids.append(subnet_id)
    print(f"Subnet Created in {az}: {subnet_id}")

# Step 3: Create an Internet Gateway and attach it to the VPC
igw_response = ec2_client.create_internet_gateway()
igw_id = igw_response['InternetGateway']['InternetGatewayId']
ec2_client.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
print(f"Internet Gateway Created and Attached: {igw_id}")

# Step 4: Create a Route Table, add a route to the internet, and associate it with each subnet
route_table_response = ec2_client.create_route_table(VpcId=vpc_id)
route_table_id = route_table_response['RouteTable']['RouteTableId']
ec2_client.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=igw_id, RouteTableId=route_table_id)

for subnet_id in subnet_ids:
    ec2_client.associate_route_table(SubnetId=subnet_id, RouteTableId=route_table_id)
print(f"Route Table Created and Associated with Subnets: {route_table_id}")

# Step 5: Create a Security Group
sg_response = ec2_client.create_security_group(GroupName='eks-security-group', Description='EKS Security Group', VpcId=vpc_id)
security_group_id = sg_response['GroupId']
print(f"Security Group Created: {security_group_id}")

# Add rules to the security group (adjust as necessary)
ec2_client.authorize_security_group_ingress(GroupId=security_group_id, IpPermissions=[
    {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
    {'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
])

    # Step 6: Create an IAM Role for EKS
    try:
        assume_role_policy_document = json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "eks.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        })

        role_response = iam_client.create_role(
            RoleName='MyEKSRole',
            AssumeRolePolicyDocument=assume_role_policy_document,
            Description='EKS Service Role',
        )
        role_arn = role_response['Role']['Arn']
        print(f"IAM Role Created: {role_arn}")

        # Attach the AmazonEKSClusterPolicy policy to the role
        iam_client.attach_role_policy(
            RoleName='MyEKSRole',
            PolicyArn='arn:aws:iam::aws:policy/AmazonEKSClusterPolicy'
        )
        print("AmazonEKSClusterPolicy attached to the role.")
    except Exception as e:
        print(f"Error creating IAM role for EKS: {str(e)}")

    # Wait a few seconds to ensure IAM role is propagated
    import time
    time.sleep(10)

    # Step 7: Create an EKS Cluster
    # Update the roleArn with the ARN of the newly created role
    try:
        eks_response = eks_client.create_cluster(
            name='MyEKSCluster',
            version='1.21',
            roleArn=role_arn,  # Use the ARN from the newly created role
            resourcesVpcConfig={
                'subnetIds': subnet_ids,
                'securityGroupIds': [security_group_id],
                'endpointPublicAccess': True,
                'endpointPrivateAccess': False,
            }
        )
        print(f"EKS Cluster Creation Initiated: {eks_response['cluster']['name']}")
    except Exception as e:
        print(f"Error creating EKS cluster: {str(e)}")

