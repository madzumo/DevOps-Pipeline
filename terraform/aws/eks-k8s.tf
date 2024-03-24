module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "20.8.4"

  cluster_name = var.cluster_name
  cluster_version = var.k8s_version
  cluster_endpoint_public_access = true
  # cluster_endpoint_private_access = true
  
  #Item below is needed otherwise you'd have to add IAM user in ACCESS area of the cluster
  enable_cluster_creator_admin_permissions = true
  subnet_ids = module.madzumo-ops-vpc.private_subnets
  vpc_id = module.madzumo-ops-vpc.vpc_id

   cluster_addons = {
    aws-ebs-csi-driver = {}
  } 
   tags = {
    environment = "madzumo"
    applicatiion = "ecommerce"
  }

  eks_managed_node_groups = {
    demo-node = {
      use_custom_templates = false
      instance_types       = ["t3.small"]
      node_group_name      = var.env_prefix

      min_size     = 1
      max_size     = 4
      desired_size = 3

      tags = {
        Name = "${var.env_prefix}"
      }   
      # EBS CSI Driver policy
      iam_role_additional_policies = {
        AmazonEBSCSIDriverPolicy = "arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy"
      }  
    }
  }
  # fargate_profiles = {
  #   profile = {
  #     name = "my-fargate-profile"
  #     selectors = [
  #       {
  #         namespace = "demo-ns"
  #       }
  #     ]
  #   }
  # }
}