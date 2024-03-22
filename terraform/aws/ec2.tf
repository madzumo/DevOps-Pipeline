resource "aws_security_group" "sg_madzumo_demo" {
  name        = "sg_madzumo_demo"
  description = "Terraform Security Group"
  
  vpc_id = module.madzumo-demo-vpc.vpc_id
  
  // Define ingress rules to allow SSH, HTTP, and HTTPS traffic
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    description = "HTTP"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

// ec2 instances. Jenkins
resource "aws_instance" "jenkins" {
  ami = "ami-0c1f63f548742ea43"
  instance_type = var.ec2_instance_type
  key_name = var.ec2_ssh_key_name
  associate_public_ip_address = true
  subnet_id = module.madzumo-demo-vpc.public_subnets[0]
  availability_zone = module.madzumo-demo-vpc.azs[0]
  vpc_security_group_ids = [ aws_security_group.sg_madzumo_demo.id ]
  depends_on = [ module.madzumo-demo-vpc ]
  tags = {
    Name = "${var.env_prefix}-jenkins"
  }
  
  provisioner "local-exec" {
    working_dir = "../../ansible"
    command = "ansible-playbook -i ${self.public_ip}, --private-key ${var.ssh_key_private_location} --user ec2-user deploy-jenkins.yaml"
  }
}