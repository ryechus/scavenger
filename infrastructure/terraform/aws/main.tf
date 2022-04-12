# ecr
resource "aws_ecr_repository" "scavenger_blog" {
  name                 = "scavenger_blog"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# ecs cluster
resource "aws_ecs_cluster" "scavenger" {
  name = "scavenger"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# security group
resource "aws_security_group" "allow_tls" {
  name        = "allow_tls"
  description = "Allow TLS inbound traffic"
  vpc_id      = data.aws_vpc.main.id

  ingress {
    description = "TLS from VPC"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "allow_tls"
  }
}

# s3 bucket
resource "aws_s3_bucket" "logs" {
  bucket = "scavenger-lb-logs"

  tags = {
    Environment = "development"
  }
}

#resource "aws_network_interface" "test" {
#  subnet_id       = data.aws_subnet.main.id
#}
