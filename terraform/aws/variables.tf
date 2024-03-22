#*********************************
#Globals
#*********************************
variable env_prefix {
  default = "madzumo_demo"
}
variable region {
  default = "us-east-1"
}
variable "ssh_key_private_location" {
  default = "~/.ssh/id_rsa"
}
variable "ec2_ssh_key_name" {
  default = "nana"
}
variable "ec2_instance_type" {
  default = "t3.large"
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