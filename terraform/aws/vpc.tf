provider "aws" {
  region = "us-east-1"
}

data "aws_availability_zones" "azs" {}

module "madzumo-demo-vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.6.0"

  name = "madzumo-demo-vpc"
  cidr = var.vpc_cidr_block
  private_subnets = var.private_subnet_cidr_blocks
  public_subnets = var.public_subnet_cider_blocks
  azs = data.aws_availability_zones.azs.names
  enable_nat_gateway = true
  single_nat_gateway = true
  enable_dns_hostnames = true

  tags = {
    "Name" = "madzumo-vpc"
  }
}