# ecs task definition
resource "aws_ecs_task_definition" "scavenger" {
  family                   = "service"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = data.aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_execution_role.arn
  container_definitions = jsonencode([
    {
      name      = "scavenger"
      image     = "188863028714.dkr.ecr.us-west-1.amazonaws.com/scavenger_blog:${var.source_code_version}"
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
      environment = [
        {
          name  = "DB_NAME",
          value = "scavenger"
        },
        {
          name  = "DB_USER",
          value = "scavenger",
        },
        {
          name  = "DB_PASS",
          value = "scavenger"
        },
        {
          name  = "DB_HOST",
          value = "terraform-20220319082057909300000001.cqautf7pxlyd.us-west-1.rds.amazonaws.com"
        },
        {
          name  = "DJANGO_SECRET_KEY",
          value = random_password.django_secret_key.result
        },
        {
          name  = "DJANGO_SETTINGS_MODULE"
          value = "scavenger.settings.production"
        }
      ]
    }
  ])
}