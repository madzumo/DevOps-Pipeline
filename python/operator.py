import python.ec2_config as ec2_config

class OperatorEc2(ec2_config.Ec2Config):
    def __init__(self, key_id='', secret_id='', region="us-east-1", instance_name=''):
        super().__init__(key_id, secret_id, region, instance_name)
        self.terraform_file_location = ''
        self.ansible_playbook_location = ''
        
    def terraform_install(self):
        True
        
    def ansible_install(self):
        True
    
    def terraform_eks_cluster_up(self):
        True
    
    def ansible_ecommerce_site_apply(self):
        True
        
    def output_review(self):
        True
    
    def terraform_eks_cluster_down(self):
        True