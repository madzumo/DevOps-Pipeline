# import python.aws_madzumo as aws_madzumo
import python.aws_madzumo as aws_madzumo
import python.operator as operator

def main():
    # 1. Check & Setup AWS connection
    aws_conn = aws_madzumo.AWSbase()
    
    while not aws_conn.check_aws_credentials():
        aws_conn.get_aws_credentails()
        aws_conn.set_aws_env_vars()

    # 2. Create node Instance (Terraform & Ansible control node)
    control_node_instance = operator.OperatorEc2()
    control_node_instance.create_ec2_instance('madzumo-Operator')
    print(f"Node Operator Created\n{control_node_instance.ec2_instance_public_ip}\n{control_node_instance.ec2_instance_public_dnsname}")
    
    # 3. Install Terraform & Anssible on Control Node
    control_node_instance.install_terraform()
    control_node_instance.install_ansible()
    
    # 4. use Terraform to deploy eks cluster
    control_node_instance.terraform_eks_cluster_up
    
    # 5. use Ansible to apply cluster with k8s ecommerce.yaml
    control_node_instance.ansible_ecommerce_site_apply()
    
    # 6. Display Review of install to user
    control_node_instance.output_review()
    
    # 7. Clean up all objections & remove instances
    control_node_instance.terraform_eks_cluster_down()
    # control_node_instance.delete_ec2_instance()
    
if __name__ == "__main__":
    main()