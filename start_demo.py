import python.aws_madzumo as aws_madzumo
import python.operator as operator
import os

def main():
    # 1. Check & Setup AWS connection
    aws_conn = aws_madzumo.AWSbase()
    
    while not aws_conn.check_aws_credentials():
        aws_conn.get_aws_credentails()
        aws_conn.set_aws_env_vars()

    # 2. Create Operator Node Instance (Terraform & Ansible control node)
    operator_instance = operator.OperatorEc2()
    operator_instance.create_ec2_instance('madzumo-ops')
    
    # 3. Install Terraform & Anssible on Operator Node
    operator_instance.deploy_terraform_ansible()
    
    # 4. use Terraform to deploy eks cluster
    operator_instance.terraform_eks_cluster_up()
    
    # # 5. use Ansible to apply cluster with k8s ecommerce.yaml
    # operator_instance.ansible_ecommerce_site_apply()
    
    # # 6. Display Review of install to user
    # operator_instance.output_review()
    
    # # 7. Clean up all objections & remove instances
    # operator_instance.terraform_eks_cluster_down()
    # # control_node_instance.delete_ec2_instance()
    
if __name__ == "__main__":
    main()