import time
import helper_config as hc
import boto3

from ec2_config import Ec2Config
from ssh_client import SSHClient
from kubernetes import client, config


class OperatorEc2(Ec2Config):
    def __init__(self, instance_name, key_id='', secret_id='', region="us-east-1"):
        super().__init__(instance_name, key_id, secret_id, region)
        self.terraform_file_location = ''
        self.ansible_playbook_location = ''
        self.k8_website = ''
        self.ansible = ''
        self.prometheus = 'coming soon'
        self.jenkins = 'coming soon'
        self.grafana = 'coming soon'

    def install_terraform_ansible(self):
        hc.console_message(["Install Terraform + Ansible + Helm"], hc.ConsoleColors.info)
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
        curl -LO https://get.helm.sh/helm-v3.14.3-linux-amd64.tar.gz
        tar -zxvf helm-v3.14.3-linux-amd64.tar.gz
        sudo mv linux-amd64/helm /usr/local/bin/helm
        """
        # print(f"What we have\n{self.ec2_instance_public_ip}\n{self.ssh_username}\n{self.ssh_key_path}")
        ssh_run = SSHClient(self.ec2_instance_public_ip, self.ssh_username, self.ssh_key_path)
        ssh_run.run_command(install_script)

    def terraform_eks_cluster_up(self):
        hc.console_message(["Initialize Terraform"], hc.ConsoleColors.info)
        install_script = """
        terraform -chdir=madzumo/terraform/aws init
        """
        ssh_run = SSHClient(self.ec2_instance_public_ip, self.ssh_username, self.ssh_key_path)
        ssh_run.run_command(install_script)

        hc.console_message(["Deploy Infrastructure via Terraform"], hc.ConsoleColors.info)
        hc.console_message(["Waiting on cluster(10 min) Please Wait!"], hc.ConsoleColors.info, total_chars=0)
        install_script = """
        terraform -chdir=madzumo/terraform/aws apply -auto-approve
        """
        ssh_run = SSHClient(self.ec2_instance_public_ip, self.ssh_username, self.ssh_key_path)
        ssh_run.run_command(install_script)

    def ansible_apply_playbook(self):
        hc.console_message(["Deploy app via Ansible on Kubernetes Cluster"], hc.ConsoleColors.info)
        install_script = f"""
        ansible-galaxy collection install community.kubernetes
        aws eks --region {self.region} update-kubeconfig --name madzumo-ops-cluster
        ansible-playbook madzumo/ansible/deploy-web.yaml
        """
        ssh_run = SSHClient(self.ec2_instance_public_ip, self.ssh_username, self.ssh_key_path)
        ssh_run.run_command(install_script)

    def install_prometheus_grafana(self): # handed off to Ansible to control
        hc.console_message(["Deploy Prometheus and Setup Grafana"], hc.ConsoleColors.info)
        install_script = """
                helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
                helm repo update
                kubectl create namespace monitoring
                helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring
                """
        ssh_run = SSHClient(self.ec2_instance_public_ip, self.ssh_username, self.ssh_key_path)
        ssh_run.run_command(install_script)
        # Check status: kubectl --namespace monitoring get pods -l "release=monitoring"
        # kubectl port-forward service/monitoring-kube-prometheus-prometheus -n monitoring 9090:9090 &
        # ps aux | grep kubectl | grep port-forward
        # kill <PID>
        # Grafana: admin / prom-operator
        # Test traffic:
        # kubectl run curl-test --image=radial/busyboxplus:curl -i --tty --rm

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

    def get_web_url(self):
        try:
            install_script = """
                    kubectl get svc frontend -o=jsonpath='{.status.loadBalancer.ingress[0].hostname}' -n madzumo-ops
                    """
            # print(self.ec2_instance_public_ip)
            # print(self.ssh_username)
            # print(self.ssh_key_path)
            ssh_run = SSHClient(self.ec2_instance_public_ip, self.ssh_username, self.ssh_key_path)
            ssh_run.run_command(install_script, show_output=False)
            self.k8_website = f"http://{ssh_run.command_output}"
            return True
        except Exception as ex:
            print(f"Get web URl Error:\n{ex}")
            return False

    def get_prometheus_url(self):
        try:
            install_script = """
                    kubectl get svc monitoring-kube-prometheus-prometheus -o=jsonpath='{.status.loadBalancer.ingress[0].hostname}' -n monitoring
                    """
            # print(self.ec2_instance_public_ip)
            # print(self.ssh_username)
            # print(self.ssh_key_path)
            ssh_run = SSHClient(self.ec2_instance_public_ip, self.ssh_username, self.ssh_key_path)
            ssh_run.run_command(install_script, show_output=False)
            self.prometheus = f"http://{ssh_run.command_output}"
            return True
        except Exception as ex:
            print(f"Get web URl Error:\n{ex}")
            return False
    
    def get_grafana_url(self):
        try:
            install_script = """
                    kubectl get svc monitoring-grafana -o=jsonpath='{.status.loadBalancer.ingress[0].hostname}' -n monitoring
                    """
            # print(self.ec2_instance_public_ip)
            # print(self.ssh_username)
            # print(self.ssh_key_path)
            ssh_run = SSHClient(self.ec2_instance_public_ip, self.ssh_username, self.ssh_key_path)
            ssh_run.run_command(install_script, show_output=False)
            self.grafana = f"http://{ssh_run.command_output}"
            return True
        except Exception as ex:
            print(f"Get web URl Error:\n{ex}")
            return False
        
    def terraform_eks_cluster_down(self):
        hc.console_message(["Removing e-commerce app from EKS Cluster"], hc.ConsoleColors.info)
        install_script = """
        ansible-playbook madzumo/ansible/remove-web.yaml
        """
        ssh_run = SSHClient(self.ec2_instance_public_ip, self.ssh_username, self.ssh_key_path)
        ssh_run.run_command(install_script)
        time.sleep(10)
        hc.console_message(["Removing EKS Cluster & other resources (10 min)", "Please Wait!"],
                           hc.ConsoleColors.info)
        install_script = """
        terraform -chdir=madzumo/terraform/aws destroy -auto-approve
        """
        ssh_run = SSHClient(self.ec2_instance_public_ip, self.ssh_username, self.ssh_key_path)
        ssh_run.run_command(install_script)

        hc.console_message(["All resources for EKS cluster removed"], hc.ConsoleColors.info)

    def get_cluster_status(self):
        try:
            eks_client = boto3.client('eks')
            response = eks_client.describe_cluster(name='madzumo-ops-cluster')
            status = response['cluster']['status']
            if str(status).lower() == 'active':
                return 'UP'
            else:
                return status

        except Exception as e:
            print(f"Error: {e}")
            return 'unknown'
