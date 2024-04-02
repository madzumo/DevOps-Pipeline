import helper_config as hc
from s3_config import S3config
from ec2_config import Ec2Config
from operator_config import OperatorEc2
from status_config import StatusPage
from enum import Enum


class MenuOptions(Enum):
    test_connection = '1'
    set_aws_creds = '2'
    setup_pipeline = '3'
    destroy_pipeline = '4'
    status_page = '5'
    quit_demo = '6'


class StartDemo:
    """main class to orchestrate the full pipeline demo"""
    def __init__(self):
        hc.display_header()
        hc.console_message(hc.welcome_message, hc.ConsoleColors.title)

        self.operator_instance = OperatorEc2('madzumo-ops')
        self.jenkins_instance = Ec2Config('madzumo-jenkins')
        self.menu = MenuOptions

    def run_demo(self):
        while True:
            hc.console_message(hc.menu_options, hc.ConsoleColors.menu, 47)
            user_option = input('')
            hc.clear_console()
            if user_option == self.menu.test_connection.value:
                self.operator_instance.check_aws_credentials()
            elif user_option == self.menu.set_aws_creds.value:
                self.operator_instance.set_aws_env_vars()
            elif user_option == self.menu.setup_pipeline.value:
                self._setup_the_show()
            elif user_option == self.menu.destroy_pipeline.value:
                self._destroy_the_show()
                hc.clear_console()
                hc.display_outro_message()
            elif user_option == self.menu.status_page.value:
                self._status_of_the_show()
            elif user_option == self.menu.quit_demo.value:
                break
            else:
                hc.console_message(['Error', 'Enter option 1-5'], hc.ConsoleColors.error, total_chars=47)
            hc.end_of_line()

    def _setup_the_show(self):
        if self._confirm_the_show():
            hc.console_message(['***Please, Do NOT Interrupt This Process***'], hc.ConsoleColors.warning, total_chars=0)
            # 1. test AWS connection
            if self.operator_instance.check_aws_credentials():
                # 2. Setup S3 bucket for storage
                s3_temp_bucket_name = f"madzumo-ops-{self.operator_instance.aws_account_number}"
                s3_setup = S3config(s3_temp_bucket_name)
                if s3_setup.check_if_bucket_exists():
                    hc.console_message(['Temp S3 bucket exists'], hc.ConsoleColors.info)
                else:
                    hc.console_message(['Creating temp S3 bucket'], hc.ConsoleColors.info)
                    s3_setup.create_bucket()
                self.operator_instance.s3_temp_bucket = s3_temp_bucket_name

                # 3. Initialize Operator Node Instance (Terraform & Ansible control node)
                hc.console_message(['Creating Operator Node'], hc.ConsoleColors.info)
                self.operator_instance.create_ec2_instance(True)

                # 4. Install Terraform & Ansible on Operator Node
                self.operator_instance.install_terraform_ansible()

                # 5. use Terraform to deploy eks cluster
                self.operator_instance.terraform_eks_cluster_up()

                # 6. use Ansible to apply full e-commerce site on k8s
                self.operator_instance.ansible_apply_playbook()

                # 7. deploy Prometheus and Grafana

                hc.console_message(['Pipeline Complete!'], hc.ConsoleColors.title)
                hc.pause_console()
                hc.clear_console()
                self._status_of_the_show()


    def _confirm_the_show(self):
        hc.console_message(['This will install the full pipeline ending with a working e-commerce website',
                            'Please do NOT interrupt this process once it begins', 'Proceed? (yes/N)'],
                           hc.ConsoleColors.title)
        response = input('')

        if response.lower() != 'y' and response.lower() != 'yes':
            hc.console_message(['Pipeline Creation Cancelled by User', '(must enter YES)'], hc.ConsoleColors.error, 0)
            return False
        else:
            hc.clear_console()
            return True

    def _destroy_the_show(self):
        # 1. test AWS connection
        if self.operator_instance.check_aws_credentials(False):
            # 2. Populate this workstation with Pipeline data
            self.operator_instance.populate_ec2_instance()

            # 3. CHECK TO SEE IF IT EXISTS YET -> Status checks first

            # 4. Clean up all Objects & remove instances
            self.operator_instance.terraform_eks_cluster_down()
            self.operator_instance.delete_ec2_instance()
            self.operator_instance.remove_local_key_pair()

            # 5. lastly, remove S3 bucket
            hc.console_message(["Terminating temp S3 bucket"], hc.ConsoleColors.info)
            s3_setup = S3config(f"madzumo-ops-{self.operator_instance.aws_account_number}")
            s3_setup.delete_bucket_contents()
            s3_setup.delete_bucket()

    def _status_of_the_show(self):
        sp = StatusPage(self.operator_instance)
        sp.populate_status_page()


if __name__ == "__main__":
    start_demo = StartDemo()
    start_demo.run_demo()
