terraform {
  backend "s3" {
    profile = "zilla"
    bucket  = "scavenger-terraform-state"
    key     = "statefiles/terraform.tfstate"
    region  = "us-west-1"
  }
}

provider "aws" {
  profile = "zilla"
  region  = "us-west-1"

  default_tags {
    tags = {
      Environment = "dev"
      Owner       = "mike"
      Project     = "scavenger"
    }
  }
}