resource "random_password" "django_secret_key" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

data "aws_db_instance" "django_db" {
  db_instance_identifier = "scavenger-dev"
}

data "aws_s3_bucket" "scavenger-django-storage" {
  bucket = "scavenger-django-storage"
}

data "aws_ecs_cluster" "scavenger" {
  cluster_name = "scavenger"
}

data "aws_lb_target_group" "cms" {
  arn = "arn:aws:elasticloadbalancing:us-west-1:188863028714:targetgroup/tf-20220323221541330000000002/ce7626a7db4d6934"
}
