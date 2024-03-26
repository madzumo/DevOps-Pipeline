import aws_madzumo
import operator_config
import helper_config as hc
import s3_config
import os

operator_instance = operator_config.OperatorEc2('madzumo-ops')


def main():
    hc.display_header()
    hc.console_message(hc.welcome_message, hc.ConsoleColors.title)
    while True:
        hc.console_message(hc.menu_options, hc.ConsoleColors.menu, 47)
        # user_option = input(Back.RED + Fore.WHITE + '')
        user_option = input('')
        hc.clear_console()
        if user_option == '1':
            operator_instance.check_aws_credentials()
        elif user_option == '2':
            operator_instance.set_aws_env_vars()
        elif user_option == '3':
            setup_the_show()
        elif user_option == '4':
            destroy_the_show()
            hc.clear_console()
            hc.display_outro_message()
        elif user_option == '5':
            status_of_the_show()
        elif user_option == '6':
            break
        else:
            hc.console_message(['Error', 'Enter option 1-5'], hc.ConsoleColors.error, total_chars=47)

        hc.end_of_line()


def setup_the_show():
    hc.console_message(['This will install the full pipeline ending with a working e-commerce website',
                        'Please do NOT interrupt this process once it begins', 'Proceed? (yes/N)'],
                       hc.ConsoleColors.title)
    response = input('')

    if response.lower() != 'y' and response.lower() != 'yes':
        hc.console_message(['Pipeline Creation Cancelled by User', '(must enter YES)'], hc.ConsoleColors.error, 0)
        return
    else:
        hc.clear_console()

    hc.console_message(['Do Not Interrupt this Process'], hc.ConsoleColors.warning, total_chars=25)
    # 1. test AWS connection
    if not operator_instance.check_aws_credentials():
        return

    # 2. Setup S3 bucket for storage
    s3_temp_bucket_name = f"madzumo-ops-{operator_instance.aws_account_number}"
    s3_setup = s3_config.S3config(s3_temp_bucket_name)
    if s3_setup.check_if_bucket_exists():
        hc.console_message(['Temp S3 bucket exists'], hc.ConsoleColors.info)
    else:
        hc.console_message(['Creating temp S3 bucket'], hc.ConsoleColors.info)
        s3_setup.create_bucket()
    operator_instance.s3_temp_bucket = s3_temp_bucket_name

    # 3. Initialize Operator Node Instance (Terraform & Ansible control node)
    hc.console_message(['Creating Operator Node'], hc.ConsoleColors.info)
    operator_instance.create_ec2_instance()

    # 4. Install Terraform & Ansible on Operator Node
    operator_instance.deploy_terraform_ansible()

    # 5. use Terraform to deploy eks cluster
    operator_instance.terraform_eks_cluster_up()

    # 6. use Ansible to apply full e-commerce site to k8s
    operator_instance.ansible_play_ecommerce()

    hc.console_message(['Pipeline Complete!'], hc.ConsoleColors.title)
    hc.pause_console()
    hc.clear_console()
    status_of_the_show()


def status_of_the_show():
    # 6. Display Review of install to user
    operator_instance.populate_ec2_instance(show_result=False)
    operator_instance.pipeline_status()


def destroy_the_show():
    # 1. test AWS connection
    if not operator_instance.check_aws_credentials():
        return

    # 2. Populate this workstation with Pipeline data
    operator_instance.populate_ec2_instance()

    # 3. Clean up all Objects & remove instances
    operator_instance.terraform_eks_cluster_down()
    operator_instance.delete_ec2_instance()
    operator_instance.remove_local_key_pair()
    # 4. lastly remove S3 bucket
    hc.console_message(["Terminating temp S3 bucket"], hc.ConsoleColors.info)
    s3_setup = s3_config.S3config(f"madzumo-ops-{operator_instance.aws_account_number}")
    s3_setup.delete_bucket_contents()
    s3_setup.delete_bucket()


if __name__ == "__main__":
    main()
