import python.ec2_config as ec2_config
import paramiko
from os import getcwd

class OperatorEc2(ec2_config.Ec2Config):
    def __init__(self, key_id='', secret_id='', region="us-east-1", instance_name=''):
        super().__init__(key_id, secret_id, region, instance_name)
        self.terraform_file_location = ''
        self.ansible_playbook_location = ''
        self.ssh_key_path = ''
        self.ssh_username = 'ec2-user'
        self.ssh_timeout = 60
    
    def deploy_terraform_ansible (self):
        self.ssh_key_path = f"{getcwd()}/{self.ec2_instance_name}-keypair"
        print("Deploying Terraform and Ansible")

        install_script = """
        rm -rf madzumo
        sudo yum update
        sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
        sudo yum -y install terraform
        sudo yum install python3
        sudo yum install python3-pip -y
        pip install ansible
        sudo yum install git -y
        git clone https://github.com/madzumo/devOps_pipeline.git madzumo
        """
        
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())        
        
        try:
            # print(f"host: {self.ec2_instance_public_ip}\nuser: {self.ssh_username}\nkeyfile: {self.ssh_key_path}")
            ssh_client.connect(hostname=self.ec2_instance_public_ip, username=self.ssh_username, key_filename=self.ssh_key_path, timeout=self.ssh_timeout)
            print("SSH connection established")

            # Execute Terraform installation script
            stdin, stdout, stderr = ssh_client.exec_command(install_script, timeout=self.ssh_timeout)
            
            # Print output
            print(stdout.read().decode())
            print(stderr.read().decode())

        finally:
            ssh_client.close()
        
    def ansible_install(self):
        print("Installing Ansbile on Operator Control Node")

    
    def terraform_eks_cluster_up(self):
        print("Deploying EKS Cluster")

        
    def ansible_ecommerce_site_apply(self):
        print("Running Ecommerce Playbook on EKS Cluster")
        
    def output_review(self):
        print("Output Review")
    
    def terraform_eks_cluster_down(self):
        print("Destroying EKS Cluster")