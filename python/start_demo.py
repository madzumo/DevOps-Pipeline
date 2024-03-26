import aws_madzumo
import operator_config
import helper_config as hc
from colorama import Fore, Back, Style

operator_instance = operator_config.OperatorEc2('madzumo-ops')


def main():
    hc.display_header()
    hc.console_message(hc.welcome_message, hc.ConsoleColors.welcome.value)
    while True:
        hc.console_message(hc.menu_options, hc.ConsoleColors.menu.value, 47)
        # user_option = input(Back.RED + Fore.WHITE + '')
        user_option = input('')
        if user_option == '1':
            hc.clear_console()
            operator_instance.check_aws_credentials()
            end_of_line()
        elif user_option == '2':
            hc.clear_console()
            setup_the_show()
            end_of_line()
        elif user_option == '3':
            hc.clear_console()
            destroy_the_show()
            end_of_line()
        elif user_option == '4':
            hc.clear_console()
            status_of_the_show()
            end_of_line()
        elif user_option == '5':
            break
        else:
            hc.console_message(['Error', 'Enter option 1-5'], hc.ConsoleColors.error.value,total_chars=47)
            end_of_line()


def setup_the_show():
    # 1. Check AWS connection
    while not operator_instance.check_aws_credentials():
        operator_instance.set_aws_env_vars()
    # 2. Initialize Operator Node Instance (Terraform & Ansible control node)
    operator_instance.create_ec2_instance()

    # # 3. Install Terraform & Ansible on Operator Node
    # operator_instance.deploy_terraform_ansible()
    #
    # # 4. use Terraform to deploy eks cluster
    # operator_instance.terraform_eks_cluster_up()
    #
    # # 5. use Ansible to apply full e-commerce site to k8s
    # operator_instance.ansible_play_ecommerce()


def status_of_the_show():
    # 6. Display Review of install to user
    operator_instance.populate_ec2_instance(show_result=False)
    operator_instance.pipeline_status()


def destroy_the_show():
    # 7. Clean up all objections & remove instances
    operator_instance.terraform_eks_cluster_down()
    operator_instance.delete_ec2_instance()


def end_of_line():
    hc.console_message(['hit enter to continue'], hc.ConsoleColors.commands.value, pause_message=True)
    hc.clear_console()
    hc.display_header()


if __name__ == "__main__":
    main()
