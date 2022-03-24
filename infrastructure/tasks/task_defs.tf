# ecs task definition
resource "aws_ecs_task_definition" "scavenger" {
  family                   = "service"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 512
  memory                   = 1024
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
          name  = "DB_NAME"
          value = "scavenger"
        },
        {
          name  = "DB_USER"
          value = "scavenger"
        },
        {
          name  = "DB_PASS"
          value = "IdKVKBEYtylmKiJv"
        },
        {
          name  = "DB_HOST"
          value = data.aws_db_instance.django_db.address
        },
        {
          name  = "DJANGO_SECRET_KEY"
          value = random_password.django_secret_key.result
        },
        {
          name  = "DJANGO_SETTINGS_MODULE"
          value = "scavenger.settings.production"
        },
        {
          name  = "AWS_S3_ACCESS_KEY_ID"
          value = aws_iam_access_key.django.id
        },
        {
          name  = "AWS_S3_SECRET_ACCESS_KEY"
          value = aws_iam_access_key.django.secret
        },
        {
          name  = "AWS_S3_STORAGE_BUCKET",
          value = "scavenger-django-storage"
        },
        {
          name  = "AWS_S3_URL"
          value = local.aws_s3_url
        }
      ]
    }
  ])
}