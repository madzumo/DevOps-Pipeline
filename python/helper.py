import pytz
import datetime

            
def _get_current_time():
    eastern = pytz.timezone('US/Eastern')
    current_time = datetime.datetime.now(eastern)
    military_time = current_time.strftime('%H:%M:%S')
    return military_time

# def _wait_for_instance_2_die():
#     for reservation in response['Reservations']:
#         for instance in reservation['Instances']:
#             instance_id = instance['InstanceId']
#             # print(instance_id)
#     new_response = ec2_client.describe_instance_status(InstanceIds=[instance_id])
#     instance_state = new_response['InstanceStatuses'][0]['InstanceState']['Name']
#     if instance_state == 'terminated':
#         create_ec2_instance()
#     elif instance_state == 'running':
#         get_instance_host_ip_info()
#         print(f"EC2 instance RUNNING with ID: {instance_id}")
#     else:
#         print(f"Unknown state of existing instance: {instance_state}")
#         sys.exit()

# def _get_ARN_info ():
#     # Create an STS client
#     sts_client = boto3.client('sts')
#     # Get caller identity
#     response = sts_client.get_caller_identity()
#     # Extract role ARN
#     role_arn = response['Arn']
#     return role_arn