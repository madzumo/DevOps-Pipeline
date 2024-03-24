import aws_madzumo
import boto3

class S3config(aws_madzumo.AWSbase):
    def __init__(self, key_id='', secret_id='', region="us-east-1"):
        super().__init__(key_id, secret_id, region)
    
    def list_s3_buckets():
        s3 = boto3.resource('s3')
        for bucket in s3.buckets.all():
            print(bucket.name)