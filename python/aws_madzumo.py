# import boto3
import os
import boto3
import configparser
import helper_config as hc


class AWSbase:
    def __init__(self, key_id='', secret_id='', region='us-east-1'):
        self.key_id = key_id
        self.secret_id = secret_id
        self.region = region
        self.instance_type = "t3.large"
        self.tag_identity_key = 'madzumo'
        self.tag_identity_value = 'demo'
        self.instance_ami = 'ami-0c101f26f147fa7fd'
        self.aws_account_number = ''

    def set_aws_env_vars(self):
        try:
            hc.console_message(['Setup AWS Credentials'], hc.ConsoleColors.title)
            self.key_id = input("Input AWS ACCESS KeY ID:\n")
            self.secret_id = input("Input AWS SECRET Key ID:\n")
            os.environ['AWS_ACCESS_KEY_ID'] = self.key_id
            os.environ['AWS_SECRET_ACCESS_KEY'] = self.secret_id
            if self.region != '':
                os.environ['AWS_DEFAULT_REGION'] = self.region
            return True
        except Exception as ex:
            hc.console_message(["Error getting aws credentials", f"{ex}"], hc.ConsoleColors.error)
            return False

    @staticmethod
    def show_aws_env_vars():
        print(f"Access:{os.environ.get('AWS_ACCESS_KEY_ID')} ")
        print(f"Secret:{os.environ.get('AWS_SECRET_ACCESS_KEY')} ")
        print(f"Region:{os.environ.get('AWS_DEFAULT_REGION')} ")

    def check_aws_credentials(self, show_result=True):
        try:
            if show_result:
                hc.console_message(["Test AWS connection"], hc.ConsoleColors.info)
            aws_client = boto3.client('iam')
            user_details = aws_client.get_user()
            account_number = user_details['User']['Arn'].split(':')[4]
            self.aws_account_number = account_number
            credentials = boto3.Session().get_credentials()
            self.key_id = credentials.access_key
            self.secret_id = credentials.secret_key
            if show_result:
                hc.console_message(["AWS Credentials valid", f"Account:{self.aws_account_number}"],
                                   hc.ConsoleColors.info)
            return True
        except Exception as ex:
            # if show_result:
            hc.console_message(["AWS Configuration not present",f"{ex}"], hc.ConsoleColors.error)
            return False

    def get_arn_role_info(self):
        sts_client = boto3.client('sts')
        response = sts_client.get_caller_identity()
        # Extract role ARN
        role_arn = response['Arn']
        return role_arn

    def get_aws_keys(self):
        aws_credentials = {}
        credentials_file = os.path.expanduser('~/.aws/credentials')

        if os.path.exists(credentials_file):
            config_parser = configparser.ConfigParser()
            config_parser.read(credentials_file)

            if 'default' in config_parser:
                aws_credentials['access'] = config_parser['default']['aws_access_key_id']
                aws_credentials['secret'] = config_parser['default']['aws_secret_access_key']

                self.key_id = aws_credentials['access']
                self.secret_id = aws_credentials['secret']
        return aws_credentials

    def get_eks_cluster_status(self, cluster_name):
        eks_client = boto3.client('eks')
        try:
            response = eks_client.describe_cluster(name=cluster_name)
            if response['cluster']:
                cluster_status = str(response['cluster']['status']).lower
                if cluster_status == 'active':
                    return True
                else:
                    return False
        except Exception as ex:
            hc.console_message(["Error:", f"{ex}"], hc.ConsoleColors.error)
            return True
