resource "aws_db_instance" "django_db" {
  identifier          = "scavenger-${local.env}"
  allocated_storage   = 5
  engine              = "postgres"
  engine_version      = "14.2"
  instance_class      = "db.t3.micro"
  db_name             = "scavenger"
  username            = "scavenger"
  password            = random_password.db_password.result
  skip_final_snapshot = true
  publicly_accessible = true
}
