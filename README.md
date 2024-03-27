# DevOps CI/CD Pipeline Demo

**FULLY automated** CI/CD pipeline using various DevOps technologies. 
This deploys a cloud-first microservices e-commerce application into a Kubernetes cluster in AWS. The application is a web-based e-commerce app where users can 
browse items, add them to the cart, and purchase them.

Showcasing these skills: Jenkins, Docker, Containers, AWS coding, EKS, S3, VPC, Terraform, Ansible, Prometheus & Python.

## What Does It Do?

The flow starts with the application in the `src` folder. Once a change is committed to the `main` branch it
triggers Jenkins to retrieve a copy of the repo, build each app service in Docker containers, upload the images to a docker 
registry, triggers Terraform and hands off to Ansible. Terraform builds the infrastructure for the application which includes a custom VPC, EKS cluster 
S3 bucket, several EC2 instances & all security components. Once Terraform is complete, Ansible reads the
new K8s images and deploys the application with all the services to the newly created EKS cluster. 

This is an overview explanation of how the CI/CD pipeline would normally function in a private environment. 
For the purpose of this demonstration Jenkins only creates the containers and uploads to a Docker registry. The other triggers are
handled by the demo utility itself using Python. The end result is the deployment of a microservice
e-commerce web application from scratch **Fully Automated**. Below are all the individual application services that will get 
installed as containers in the Kubernetes environment. 

![micro_service](media/microsevice.png)

## Prerequisites

1. All you need is an Access Key ID and Secret Key ID. However, it's best if you download and install the AWS CLI tool and run
`aws configure` from the command line. This will ask for the Access Key ID and Secret Key ID as well as the region to statically set it
on your workstation. 
2. This pipeline is configured of many technologies and accesses many components, so it is highly recommended that your Access & Secret ID user have **administrator rights** to the  AWS environment.

## Download 

[DevOps Demo - Windows](media/madzumo_devops.zip)

## How to use

This is a self-contained demo utility. Everything needed to showcase the above technologies is included. Download for your OS, unzip and execute **`start_demo.exe`**. 
You will have the following menu options.

![Menu](media/menu.png)

- **Test AWS Connection** - Test connectivity to your AWS environment. If you have aws cli installed and configured then 
    it will automatically connect. Otherwise, you will need to enter your Access Key & Secret Key using the next option.
- **Set AWS Credentials** - Allows you to manually enter your AWS Access Key & Secret Key. It's good while the application 
      is open and you will have to re-enter upon each execution. That is why it's better to install the AWS CLI utility 
      beforehand and run `aws configure` in the command line.
- **Install Full Pipeline** - Exactly what it says. Install all components for a full CI/CD pipeline with all the technology stated above. **Fully Automated**
- **Remove Existing Pipeline** - This removes all components and resources installed in the option above leaving your AWS environment clean.
- **View Pipeline Status** - Here you can view the custom URL created for the e-commerce website so you can test its functionality.
      In addition,  the status of your cluster and IP address of your Operator Node will be displayed.  You can run this anytime and 
      from any computer. As long as your AWS credentials are valid to the same environment then you will see the same status information.

