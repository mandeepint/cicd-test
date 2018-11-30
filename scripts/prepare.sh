#!/bin/sh

sudo yum update -y
sudo yum install -y docker
sudo curl -L "https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /opt/bin/docker-compose
sudo chmod +x /opt/bin/docker-compose
newgrp docker
sudo usermod -a -G docker ec2-user
chown -R ec2-user:ec2-user /artemis