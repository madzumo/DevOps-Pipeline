import python.ec2_config as ec2_config
from os import getcwd
from python.ssh_client import SSHClient

class OperatorEc2(ec2_config.Ec2Config):
    def __init__(self, key_id='', secret_id='', region="us-east-1", instance_name=''):
        super().__init__(key_id, secret_id, region, instance_name)
        self.terraform_file_location = ''
        self.ansible_playbook_location = ''
    
    def deploy_terraform_ansible (self):
        print("Deploying Terraform and Ansible")
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
        ssh_run = SSHClient(self.ec2_instance_public_ip,self.ssh_username,self.ssh_key_path)
        ssh_run.run_command(install_script)
        
    def terraform_eks_cluster_up(self):
        print("Initialize Terraform")
        install_script = """
        terraform -chdir=madzumo/terraform/aws init
        """
        ssh_run = SSHClient(self.ec2_instance_public_ip,self.ssh_username,self.ssh_key_path)
        ssh_run.run_command(install_script)
        
        print("Apply Terraform script")
        print("Waiting on cluster(10 min). Please wait.........")
        install_script = """
        terraform -chdir=madzumo/terraform/aws apply -auto-approve
        """
        ssh_run = SSHClient(self.ec2_instance_public_ip,self.ssh_username,self.ssh_key_path)
        ssh_run.run_command(install_script)
        
        
    def ansible_play_ecommerce(self):
        print("Running Ansible Playbook on EKS Cluster")
        # print(f"ansible-playbook -i {self.ec2_instance_public_ip} -e ansible_ssh_private_key_file={self.ssh_key_path} madzumo/ansible/deploy-web.yaml")
        install_script =f"""
        ansible-galaxy collection install community.kubernetes
        aws eks --region {self.region} update-kubeconfig --name madzumo-ops-cluster
        ansible-playbook madzumo/ansible/deploy-web.yaml
        """
        ssh_run = SSHClient(self.ec2_instance_public_ip,self.ssh_username,self.ssh_key_path)
        ssh_run.run_command(install_script)
        
    def output_review(self):
        print("Output Review")
    
    def terraform_eks_cluster_down(self):
        print("Removing e-commerce site from EKS Cluster")
        install_script = """
        ansible-playbook madzumo/ansible/remove-web.yaml
        """
        ssh_run = SSHClient(self.ec2_instance_public_ip,self.ssh_username,self.ssh_key_path)
        ssh_run.run_command(install_script)
        
        print("Removing EKS Cluster, VPC & all associated resources (10 min)")
        print("Please wait...........")
        install_script = """
        terraform -chdir=madzumo/terraform/aws destroy -auto-approve
        """
        ssh_run = SSHClient(self.ec2_instance_public_ip,self.ssh_username,self.ssh_key_path)
        ssh_run.run_command(install_script)

        print("Cluster & VPC removed")