# import boto3
import os
import boto3

class AWSbase:
    def __init__(self, key_id='', secret_id='', region = "us-east-1"):
        self.key_id = key_id
        self.secret_id = secret_id
        self.region = region
        self.instance_type = "t3.large"
        self.tag_identity_key = 'madzumo'
        self.tag_identity_value = 'demo'
        self.instance_ami = 'ami-0c101f26f147fa7fd'

    def set_aws_env_vars (self):
        os.environ['AWS_ACCESS_KEY_ID'] = self.key_id
        os.environ['AWS_SECRET_ACCESS_KEY'] = self.secret_id
        if self.region != '':
            os.environ['AWS_DEFAULT_REGION'] = self.region
    
    def show_aws_env_vars(self):
        print(f"Access:{os.environ.get('AWS_ACCESS_KEY_ID')} ")
        print(f"Secret:{os.environ.get('AWS_SECRET_ACCESS_KEY')} ")
        print(f"Region:{os.environ.get('AWS_DEFAULT_REGION')} ")
    
    def check_aws_credentials(self):
        try:
            print("Checking AWS connection......")
            aws_client= boto3.client('iam')
            user_details = aws_client.get_user()
            account_number = user_details['User']['Arn'].split(':')[4]
            print(f"AWS Credentials Found\nAccount:{account_number}")
            return True
        except Exception:
            print("AWS credentials are invalid or missing")
            return False
    
    def get_aws_credentails(self):
        try:
            self.key_id = input("Input AWS ACCESS KeY ID (quit to exit):\n")
            if self.key_id.lower == 'quit':
                exit()
            else:
                self.secret_id = input("Input AWS SECRET Key ID (quit to exit):\n")
                if self.secret_id.lower == 'quit':
                    exit()
                else:
                    self.region = input("Input Region (default: us-east-1):\n")
        except Exception as ex:
            print(f"Error getting aws credentials\n{ex}")