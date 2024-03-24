provider "aws" {
  region = "us-east-1"
}

data "aws_availability_zones" "azs" {}

#I'm not sure about this part
resource "random_string" "suffix" {
  length  = 8
  special = false
}

locals {
  cluster_name = var.cluster_name 
}

module "madzumo-ops-vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.7.0"

  name = "madzumo-ops-vpc"
  cidr = var.vpc_cidr_block
  private_subnets = var.private_subnet_cidr_blocks
  public_subnets = var.public_subnet_cider_blocks
  azs = data.aws_availability_zones.azs.names
  enable_nat_gateway = true
  single_nat_gateway = true
  enable_dns_hostnames = true

  #required tags for VPC to connect to Kubernetes
  tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
  }

  public_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/elb" = 1
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb" = 1
  }
}