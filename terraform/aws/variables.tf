#*********************************
#eks-k8s.tf (Kubernetes)
#*********************************
variable env_prefix {
  default = "madzumo-ops"
}
variable k8s_version {
  default = "1.29"
}
variable cluster_name {
  default = "madzumo-cluster"
}
variable region {
  default = "us-east-1"
}

#*********************************
#VPC.tf
#*********************************
variable "vpc_cidr_block" {
    default = "10.0.0.0/16"
}
variable "private_subnet_cidr_blocks"{
    default = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}
variable "public_subnet_cider_blocks" {
    default = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
}