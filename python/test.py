import boto3

ec2 = boto3.client('ec2')

response = ec2.describe_instances(
    Filters=[
        {
            'Name': 'tag:madzumo',
            'Values': ['demo']
        }
    ]
)

if response['Reservations']:
    print('yes')
else:
    print('no')