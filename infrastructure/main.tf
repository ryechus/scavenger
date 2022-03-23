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

# ecs service
resource "aws_ecs_service" "scavenger" {
  name                       = "scavenger-bblog"
  cluster                    = aws_ecs_cluster.scavenger.id
  task_definition            = aws_ecs_task_definition.scavenger.arn
  desired_count              = 1
  deployment_maximum_percent = 200
  launch_type                = "FARGATE"
  network_configuration {
    subnets          = ["subnet-28a2344e", "subnet-a8d173f2"]
    assign_public_ip = true
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.cms.arn
    container_name   = "scavenger"
    container_port   = 8000
  }
}

data "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRole"
}

data "aws_iam_policy" "managed_role_policy" {
  arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role" "ecs_execution_role" {
  name = "ecs_task_execution_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
        "Effect": "Allow",
        "Principal": {
         "Service": "ecs-tasks.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "ecs_attachment" {
  role       = aws_iam_role.ecs_execution_role.name
  policy_arn = data.aws_iam_policy.managed_role_policy.arn
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "role-name"

  assume_role_policy = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": "sts:AssumeRole",
     "Principal": {
       "Service": "ecs-tasks.amazonaws.com"
     },
     "Effect": "Allow",
     "Sid": ""
   }
 ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "ecs-task-execution-role-policy-attachment" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
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
