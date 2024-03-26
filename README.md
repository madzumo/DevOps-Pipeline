# DevOps CI/CD Pipeline Demo

Full CI/CD pipeline showcasing various DevOps technologies. 
This deploys a micro-service e-commerce application into a Kubernetes cluster in AWS. **FULLY automated.**

The following technologies are showcased here: Jenkins, Docker, Containers, AWS coding, EKS, S3, VPC, Terraform, Ansible, Prometheus & Python.

## Prerequisites

1. All you need is an Access Key ID and Secret Key ID. However, it's best if you download and install the AWS CLI tool and run
`aws configure` from the command line. This will ask for the Access Key ID and Secret Key ID as well as the region to statically set it
on your workstation. 
2. This pipeline is configured
of many components so it's highly recommended for this user to have **administrator rights** to the  AWS environment.

## Download 

[Devops Demo - Windows](media/devops_demo.zip)

[Devops Demo - Linux](media/devops_demo_linux.zip)

## How to use

This is a self-contained demo utility. Download for your OS, unzip and execute **start_demo.exe**. You will see menu items

![Menu](media/menu.png)

- **Test AWS Connection** - test connectivity to your AWS environment. If you have aws cli installed and configured then 
    it will automatically connect. Otherwise you will need to enter your Access Key & Secret Key using the next option
- **Set AWS Credentials** - Allows you to manually enter your AWS Access Key & Secret Key. It's good while the application 
      is open and you will have to re-enter upon each execution. That is why it's better to install the AWS cli utility 
      beforehand and run `aws configure` in the command line.
- **Install Full Pipeline** - Exactly what it says. Install all components for a full CI/CD pipeline with all the technology stated above. **Fully Automated**
- **Remove Existing Pipeline** - This removes the EKS cluster and all components associated with it leaving your AWS environment clean.
- **View Pipeline Status** - Here you can view the custom URL created for the e-commerce website so you can test its functionality
      You will also view the status of your cluster and IP address of your Operator Node.  You can run this anytime and 
      from any computer. As long as your AWS credentials are valid you will see the same status information.

## What Does this Demo do?

The flow starts with this repo. The code is located in the `src` folder. Once a change is committed to `main` branch it then
triggers Jenkins to retrieve a copy of the repo and build each service in Docker containers, uploads the images to a repo 
and triggers Terraform. Terraform builds the infrastructure for the application which includes a custom VPC, EKS cluster 
& all security components. Once Terraform is complete, Ansible reads the
new K8s images and pushes them to the newly created EKS cluster. 

In this demo, the majority of Jenkins work is being performed by this utility
using Python. For the purpose of this demonstration Jenkins is installed to create the Docker containers only but this is
an overview explanation of how the CI/CD pipeline would normally function in a private environment. The end result is the deployment of a micro-service 
e-commerce website application. Below are all the applications that will get installed as containers in the custom Kubernetes environment. 

![micro_service](media/microsevice.png)