# DevOps CI/CD Pipeline Demo

I have developed a **FULLY automated** CI/CD pipeline demo using various DevOps technologies. 
It deploys a cloud-first microservices e-commerce application into a Kubernetes cluster in AWS.
The application is a web-based e-commerce app where users can 
browse items, add them to the cart, and purchase them.
Below is the pipeline tree showing all the tech used for this demo.

![pipeline tree](media/pipeline2.jpg)

## Pipeline Flow

The flow starts with the application in the `src` folder of this repo.
Once a change is committed to the `main` branch it
triggers Jenkins to retrieve a copy of the repo,
build each app service in Docker images, upload the images to a docker 
registry, triggers Terraform and hands off to Ansible.
Terraform builds the infrastructure for the application which includes an isolated VPC, EKS cluster 
S3 bucket, EC2 instance & all security components.
Once Terraform is complete, Ansible reads the
new K8s images and deploys the application with all the services to the newly created EKS cluster. 

Python executes several triggers for the sake of this demonstration.
In a production environment, Jenkins would normally handle most of the hand-offs.
Either way, the result is the deployment of a microservice e-commerce web application from scratch **Fully Automated**. 

![website](media/site2.png)

Once complete, you will have IP access to several instances. The newly created e-commerce site to test out its functionality,
the jenkins server to view the configured pipeline, grafana charts to monitor the cluster, 
and an Operator Node to view both Terraform/Ansible configurations.
Below are the individual application service pods that will get 
installed in the Kubernetes environment. 

![services](media/microsevice2.png)

## Prerequisites

1. All you need is an AWS **Access Key ID** and **Secret Key ID** 
2. This pipeline is accessing many components in your AWS environment, so it is highly recommended that your Access & Secret ID user have **Administrator rights** to the AWS environment.

## Setup / Install 

### Option 1: Windows

1. Download and install AWS CLI here: 
    [awscli](https://awscli.amazonaws.com/AWSCLIV2.msi)
2. Download the self executable package from release link here:
    [Download -> DevOps Demo - Windows](https://github.com/madzumo/devOps-pipeline/releases/download/1.0/madzumo_devops.zip)
3. Unzip 
4. Execute **`start_demo.exe`**

### Option 2: Docker

1. Run the following container in interactive mode
```shell
docker run -it --name devopsdemo madzumo/devops-pipeline
```

## How to use

You will have the following menu options.

![menu_options](media/menu2.png)

1. **Test AWS Connection** - Test connectivity to your AWS environment.
  If you have AWS CLI installed and configured, then 
    it will automatically connect.
  Otherwise, you will need to enter your Access Key & Secret Key using the next option.
---
2. **Set AWS Credentials** - Manually enter your AWS Access Key ID & Secret Key ID.
  For the Windows option, they are set in you AWS CLI config file. For the docker option, If you run the container on each run instead of using the same container then 
you will have to re-enter these keys. To avoid having to re-enter those keys use the following commands to start the existing container you have already run and connect to it.
```shell
docker start devopsdemo
docker exec -it devopsdemo python3 start_demo.py
```
---
3. **Install Full Pipeline** - This is the main option that installs all components, as illustrated above, to create a complete CI/CD pipeline. **Fully Automated**
---
4. **Remove Existing Pipeline** - Removes all components and resources related to this demo leaving your AWS environment clean.
---
5. **View Pipeline Status** -
  View the custom URL created for the e-commerce website, the status of your cluster,
  the endpoint of your EKS cluster, the IP address of the Operator Node and the URL for the Jenkins Server.
  You can run this anytime and from any computer.
  As long
  as the AWS credentials used have access to the same environment the pipeline was created in then you will see the same status information.

