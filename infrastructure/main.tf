terraform {
  backend "s3" {
    profile = "zilla"
    bucket  = "scavenger-terraform-state"
    key     = "statefiles/terraform.tfstate"
    region  = "us-west-1"
  }
}

# provider
provider "aws" {
  profile = "zilla"
  region  = "us-west-1"
}

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
  name            = "scavenger-bblog"
  cluster         = aws_ecs_cluster.scavenger.id
  task_definition = aws_ecs_task_definition.scavenger.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets = ["subnet-28a2344e", "subnet-a8d173f2"]
    assign_public_ip = true
  }
}

data "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRole"
}

# ecs task definition
resource "aws_ecs_task_definition" "scavenger" {
  family                   = "service"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  container_definitions = jsonencode([
    {
      name      = "scavenger"
      image     = "188863028714.dkr.ecr.us-west-1.amazonaws.com/scavenger_blog:0f27020cb0df2662bc1bd5f28eb378e7d082f47a"
      command   = ["./manage.py", "runserver", "0.0.0.0:8000"]
      cpu       = 256
      memory    = 512
      essential = true
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }
      ]
    }
  ])
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
