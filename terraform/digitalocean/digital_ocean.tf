terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "2.34.1"
    }
  }
}

variable "do_token" {
  default = ""
}

provider "digitalocean" {
  token = var.do_token
}

# Create a droplet server for Jenkins or Nexus or whatever
resource "digitalocean_droplet" "droplet" {
  name   = "terraform-droplet-jenkins"
  image  = "ubuntu-23-10-x64"
  region = "nyc3"
  size   = "s-4vcpu-8gb"
  ssh_keys = [data.digitalocean_ssh_key.wsl.id]
  # user_data = file("do-scripts.sh")
  #handling this with Ansible now
  # user_data = <<-EOF
  #             #!/bin/bash
  #             - sudo apt update -y
  #             - sudo apt install docker.io -y
  #             - sudo systemctl start docker
  #             EOF
}

data "digitalocean_ssh_key" "wsl"{
  name = "wslmadzumo"
}

resource "digitalocean_firewall" "jenkins_firewall" {
  name = "jenkins-firewall-terraform"

  droplet_ids = [digitalocean_droplet.droplet.id]

  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule { #for jenkins
    protocol         = "tcp"
    port_range       = "8080"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule { #for nexus
    protocol         = "tcp"
    port_range       = "8081"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "50000"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule { #misc java app
    protocol         = "tcp"
    port_range       = "7048"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}

output "droplet-IP"{
  value = digitalocean_droplet.droplet.ipv4_address
}