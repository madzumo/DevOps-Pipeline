import time

import ec2_config
import ssh_client
from kubernetes import client, config
import helper_config as hc
import boto3
from colorama import Back, Fore, Style


class OperatorEc2(ec2_config.Ec2Config):
    def __init__(self, instance_name, key_id='', secret_id='', region="us-east-1"):
        super().__init__(instance_name, key_id, secret_id, region)
        self.terraform_file_location = ''
        self.ansible_playbook_location = ''
        self.k8_website = ''
        self.ansible = ''
        self.prometheus = 'coming soon'
        self.jenkins = 'coming soon'

    def deploy_terraform_ansible(self):
        hc.console_message(["Deploying Terraform and Ansible"], hc.ConsoleColors.info)
        self.get_aws_keys()

        install_script = f"""
        sudo yum update
        sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
        sudo yum -y install terraform
        sudo yum install python3
        sudo yum install python3-pip -y
        pip install ansible
        pip install kubernetes
        sudo yum install git -y
        if [ ! -d "madzumo" ]; then
            git clone https://github.com/madzumo/devOps_pipeline.git madzumo
        else
            echo "madzumo folder already exists."
        fi
        aws configure set aws_access_key_id {self.key_id}
        aws configure set aws_secret_access_key {self.secret_id}
        aws configure set default.region {self.region}
        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
        sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
        """
        # print(f"What we have\n{self.ec2_instance_public_ip}\n{self.ssh_username}\n{self.ssh_key_path}")
        ssh_run = ssh_client.SSHClient(self.ec2_instance_public_ip, self.ssh_username, self.ssh_key_path)
        ssh_run.run_command(install_script)

    def terraform_eks_cluster_up(self):
        hc.console_message(["Initialize Terraform"], hc.ConsoleColors.info)
        install_script = """
        terraform -chdir=madzumo/terraform/aws init
        """
        ssh_run = ssh_client.SSHClient(self.ec2_instance_public_ip, self.ssh_username, self.ssh_key_path)
        ssh_run.run_command(install_script)

        hc.console_message([''], hc.ConsoleColors.basic)
        time.sleep(5)
        hc.console_message(["Apply Terraform script", "Waiting on cluster(10 min) Please Wait!"],
                           hc.ConsoleColors.info)
        hc.console_message([''], hc.ConsoleColors.basic)
        install_script = """
        terraform -chdir=madzumo/terraform/aws apply -auto-approve
        """
        ssh_run = ssh_client.SSHClient(self.ec2_instance_public_ip, self.ssh_username, self.ssh_key_path)
        ssh_run.run_command(install_script)
        time.sleep(5)

    def ansible_play_ecommerce(self):
        hc.console_message(["Running Ansible Playbook on EKS Cluster"], hc.ConsoleColors.info)
        install_script = f"""
        ansible-galaxy collection install community.kubernetes
        aws eks --region {self.region} update-kubeconfig --name madzumo-ops-cluster
        ansible-playbook madzumo/ansible/deploy-web.yaml
        """
        ssh_run = ssh_client.SSHClient(self.ec2_instance_public_ip, self.ssh_username, self.ssh_key_path)
        ssh_run.run_command(install_script)

    def get_k8_service_hostname(self):
        hc.console_message(['Get FrondEnd Hostname'], hc.ConsoleColors.info)
        # ***ONLY WORKS AFTER AWS KUBECONFIG SETUP ON LOCAL****
        config.load_kube_config()
        v1 = client.CoreV1Api()
        namespace = "madzumo-ops"  # Adjust as needed
        service_name = "frontend"  # Replace with your service's name

        try:
            # Query the service by name
            service = v1.read_namespaced_service(name=service_name, namespace=namespace)
            print(f"Service {service_name} details:")
            print(f"UID: {service.metadata.uid}")
            print(f"Service Type: {service.spec.type}")
            print(f"Cluster IP: {service.spec.cluster_ip}")

            service_address = service.spec.cluster_ip
            if service_address is None:
                service_address = service.spec.external_ip
            if service_address is None:
                service_address = service.spec.load_balancer_ip
            if service_address is None:
                service_address = service.spec.external_name
            print(f"{service_address}")

        except client.exceptions.ApiException as e:
            print(f"An error occurred: {e}")

    def pipeline_status(self):
        # AWS status
        aws_conn_title = Back.BLACK + Fore.LIGHTWHITE_EX + Style.BRIGHT + '       AWS Connection:'
        aws_conn_status = Back.BLACK + Fore.LIGHTRED_EX + Style.BRIGHT + 'NO CONNECTION'
        aws_conn_info = ''
        if self.check_aws_credentials(show_result=False):
            aws_conn_status = Back.BLACK + Fore.GREEN + Style.BRIGHT + 'ACTIVE' + Style.NORMAL
            aws_conn_info += Back.BLACK + Fore.LIGHTWHITE_EX + f'              Account: ' + self.aws_account_number + "\n"
            aws_conn_info += Back.BLACK + Fore.LIGHTWHITE_EX + f'               Key ID: ' + self.key_id + "\n"
            aws_conn_info += Back.BLACK + Fore.LIGHTWHITE_EX + f'            Secret ID: ' + self.secret_id

        # Check Pipeline status
        pipeline_title = Back.BLACK + Fore.LIGHTWHITE_EX + Style.BRIGHT + '             Pipeline:'
        pipeline_status = Back.BLACK + Fore.LIGHTRED_EX + Style.BRIGHT + 'NOT SETUP'
        pipeline_info = ''
        # self.download_key_pair() #unablet to download pem file without corruption of data
        if self.get_instance() and self.get_web_url():
            pipeline_status = Back.BLACK + Fore.GREEN + Style.BRIGHT + 'ACTIVE' + Style.NORMAL
            pipeline_info += Back.BLACK + Fore.LIGHTWHITE_EX + f'      e-commerce site: ' + self.k8_website + "\n"
            pipeline_info += Back.BLACK + Fore.LIGHTWHITE_EX + f'     EKS Cluster Name: ' + 'madzumo-ops-cluster' + "\n"
            pipeline_info += Back.BLACK + Fore.LIGHTWHITE_EX + f'   EKS Cluster status: ' + self.get_cluster_status() + "\n"
            pipeline_info += Back.BLACK + Fore.LIGHTWHITE_EX + f'        Operator Node: ' + self.ec2_instance_public_ip + "\n"
            pipeline_info += Back.BLACK + Fore.LIGHTWHITE_EX + f'   Prometheus Monitor: ' + self.prometheus + "\n"
            pipeline_info += Back.BLACK + Fore.LIGHTWHITE_EX + f'       Jenkins Server: ' + self.jenkins + "\n"
            pipeline_info += Back.BLACK + Fore.LIGHTWHITE_EX + f'                       ' + "username: admin" + "\n"
            pipeline_info += Back.BLACK + Fore.LIGHTWHITE_EX + f'                       ' + "password: password"

        # hc.clear_console()
        print(Back.RED + Fore.YELLOW + hc.header_art_status + Style.RESET_ALL + "\n")
        # print(Back.RED + Fore.YELLOW + header_text + "\n") # entire back is red
        print(f"{aws_conn_title} {aws_conn_status}\n{aws_conn_info}\n")
        print(f"{pipeline_title} {pipeline_status}\n{pipeline_info}")

    def get_web_url(self):
        try:
            install_script = """
                    kubectl get svc frontend -o=jsonpath='{.status.loadBalancer.ingress[0].hostname}' -n madzumo-ops
                    """
            # print(self.ec2_instance_public_ip)
            # print(self.ssh_username)
            # print(self.ssh_key_path)
            ssh_run = ssh_client.SSHClient(self.ec2_instance_public_ip, self.ssh_username, self.ssh_key_path)
            ssh_run.run_command(install_script, show_output=False)
            self.k8_website = f"http://{ssh_run.command_output}"
            return True
        except Exception as ex:
            print(f"Get web URl Error:\n{ex}")
            return False

    def terraform_eks_cluster_down(self):
        hc.console_message(["Removing e-commerce app from EKS Cluster"], hc.ConsoleColors.info)
        install_script = """
        ansible-playbook madzumo/ansible/remove-web.yaml
        """
        ssh_run = ssh_client.SSHClient(self.ec2_instance_public_ip, self.ssh_username, self.ssh_key_path)
        ssh_run.run_command(install_script)
        time.sleep(10)
        hc.console_message(["Removing EKS Cluster & other resources (10 min)", "Please Wait!"],
                           hc.ConsoleColors.info)
        install_script = """
        terraform -chdir=madzumo/terraform/aws destroy -auto-approve
        """
        ssh_run = ssh_client.SSHClient(self.ec2_instance_public_ip, self.ssh_username, self.ssh_key_path)
        ssh_run.run_command(install_script)

        hc.console_message(["All resources for EKS cluster removed"], hc.ConsoleColors.info)

    def get_cluster_status(self):
        try:
            eks_client = boto3.client('eks')

            # Retrieve the status of the cluster
            response = eks_client.describe_cluster(name='madzumo-ops-cluster')

            # Extract and return the status
            status = response['cluster']['status']
            return status

        except Exception as e:
            print(f"Error: {e}")
            return 'unknown'
