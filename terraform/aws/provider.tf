terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.40.0"
    # }
    # helm = {
    #   source = "hashicorp/helm"
    #   version = "2.12.1"
    # }
    # kubernetes = {
    #   source = "hashicorp/kubernetes"
    #   version = "2.27.0"
    # }
    # kubectl = {
    #   source = "gavinbunney/kubectl"
    #   version = "1.14.0"
    }
  }
  # #backup state to s3 bucket
  # backend "s3" {
  #   bucket = "madzumo-techworld"
  #   key = "myapp/state.tfstate"
  #   region = "us-east-1"
  # }
} 