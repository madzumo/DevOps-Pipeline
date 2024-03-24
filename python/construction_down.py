import boto3
import time

# Clients
ec2_client = boto3.client('ec2')
eks_client = boto3.client('eks')
iam_client = boto3.client('iam')

# Resource Identifiers - replace these with your actual resource IDs
cluster_name = 'MyEKSCluster'
role_name = 'MyEKSRole'
security_group_id = 'sg-xxxxxxxx'
subnet_ids = ['subnet-xxxxxxxx', 'subnet-yyyyyyyy', 'subnet-zzzzzzzz', 'subnet-aaaaaaaa']
route_table_id = 'rtb-xxxxxxxx'
internet_gateway_id = 'igw-xxxxxxxx'
vpc_id = 'vpc-xxxxxxxx'

# Step 1: Delete EKS Cluster
try:
    print(f"Deleting EKS Cluster: {cluster_name}")
    eks_client.delete_cluster(name=cluster_name)
    # Wait for the cluster to be deleted (simplified wait, consider using waiter or describe_cluster in a loop)
    print("Waiting for EKS Cluster to be deleted...")
    time.sleep(120)  # Adjust based on actual deletion time
except Exception as e:
    print(f"Error deleting EKS cluster: {str(e)}")

# Step 2: Detach IAM Role Policy and Delete IAM Role
try:
    iam_client.detach_role_policy(RoleName=role_name, PolicyArn='arn:aws:iam::aws:policy/AmazonEKSClusterPolicy')
    iam_client.delete_role(RoleName=role_name)
    print(f"IAM Role Deleted: {role_name}")
except Exception as e:
    print(f"Error deleting IAM role: {str(e)}")

# Step 3: Delete Security Group
try:
    ec2_client.delete_security_group(GroupId=security_group_id)
    print(f"Security Group Deleted: {security_group_id}")
except Exception as e:
    print(f"Error deleting security group: {str(e)}")

# Step 4: Disassociate and Delete Route Table (if applicable)
# Assuming a custom route table was used; adjust if you used the main route table

# Step 5: Detach and Delete Internet Gateway
try:
    ec2_client.detach_internet_gateway(InternetGatewayId=internet_gateway_id, VpcId=vpc_id)
    ec2_client.delete_internet_gateway(InternetGatewayId=internet_gateway_id)
    print(f"Internet Gateway Deleted: {internet_gateway_id}")
except Exception as e:
    print(f"Error deleting internet gateway: {str(e)}")

# Step 6: Delete Subnets
for subnet_id in subnet_ids:
    try:
        ec2_client.delete_subnet(SubnetId=subnet_id)
        print(f"Subnet Deleted: {subnet_id}")
    except Exception as e:
        print(f"Error deleting subnet {subnet_id}: {str(e)}")

# Step 7: Delete the VPC
try:
    ec2_client.delete_vpc(VpcId=vpc_id)
    print(f"VPC Deleted: {vpc_id}")
except Exception as e:
    print(f"Error deleting VPC: {str(e)}")
