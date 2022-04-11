resource "random_password" "db_password" {
  length  = 16
  special = false
}

data "aws_vpc" "main" {
  id = "vpc-27cd6a41"
}

data "aws_subnet" "main" {
  id = "subnet-28a2344e"
}
