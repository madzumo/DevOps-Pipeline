import aws_madzumo
import boto3
from botocore.exceptions import NoCredentialsError

class S3config(aws_madzumo.AWSbase):
    def __init__(self, key_id='', secret_id='', region="us-east-1"):
        super().__init__(key_id, secret_id, region)

    def list_s3_buckets():
        s3 = boto3.resource('s3')
        for bucket in s3.buckets.all():
            print(bucket.name)

    def create_bucket(bucket_name, region=None):
        """Create an S3 bucket in a specified region

        If a region is not specified, the bucket is created in the S3 default
        region (us-east-1).

        :param bucket_name: Bucket to create
        :param region: String region to create bucket in, e.g., 'us-west-2'
        :return: True if bucket created, else False
        """
        try:
            if region is None:
                s3_client = boto3.client('s3')
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client = boto3.client('s3', region_name=region)
                location = {'LocationConstraint': region}
                s3_client.create_bucket(Bucket=bucket_name,
                                        CreateBucketConfiguration=location)
        except NoCredentialsError:
            print("Credentials not available")
            return False
        return True

    def upload_file_to_bucket(file_name, bucket_name, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket_name: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        # Upload the file
        s3_client = boto3.client('s3')
        try:
            s3_client.upload_file(file_name, bucket_name, object_name)
        except NoCredentialsError:
            print("Credentials not available")
            return False
        return True

    # Example usage:
    bucket_name = 'madzumo-ops'
    file_name = 'path/to/your/local/file'  # Specify the path to your local file
    region = 'us-west-2'  # Specify your region

    # Create the bucket
    if create_bucket(bucket_name, region):
        print(f"Bucket '{bucket_name}' created successfully.")

        # Upload the file
        if upload_file_to_bucket(file_name, bucket_name):
            print(f"File '{file_name}' uploaded successfully to bucket '{bucket_name}'.")
    else:
        print(f"Failed to create bucket '{bucket_name}'.")

    def delete_bucket_contents(bucket_name):
        """Delete all the contents of an S3 bucket

        :param bucket_name: The name of the bucket to empty
        """
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        try:
            bucket.objects.delete()
        except NoCredentialsError:
            print("Credentials not available")
            return False
        return True

    def delete_bucket(bucket_name):
        """Delete an empty S3 bucket

        :param bucket_name: The name of the bucket to delete
        """
        s3 = boto3.client('s3')
        try:
            s3.delete_bucket(Bucket=bucket_name)
        except NoCredentialsError:
            print("Credentials not available")
            return False
        return True

    # Example usage:
    bucket_name = 'madzumo-ops'  # Specify the bucket name

    # Empty the bucket
    if delete_bucket_contents(bucket_name):
        print(f"Contents of bucket '{bucket_name}' deleted successfully.")

        # Delete the bucket
        if delete_bucket(bucket_name):
            print(f"Bucket '{bucket_name}' deleted successfully.")
    else:
        print(f"Failed to delete the contents of bucket '{bucket_name}'.")