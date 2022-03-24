terraform {
  backend "s3" {
    profile = var.aws_profile
    bucket  = "scavenger-terraform-state"
    key     = "statefiles/scavenger-tasks_terraform.tfstate"
    region  = "us-west-1"
  }
}

provider "aws" {
  profile = var.aws_profile
  region  = "us-west-1"

  default_tags {
    tags = {
      Environment = "dev"
      Owner       = "mike"
      Project     = "scavenger"
    }
  }
}