terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }

  backend "s3" {
    profile = "zilla"
    bucket  = "scavenger-terraform-state"
    key     = "statefiles/terraform-do.tfstate"
    region  = "us-west-1"
  }
}

# Set the variable value in *.tfvars file
# or using -var="do_token=..." CLI option
variable "do_token" {
  type        = string
  description = ""
}

# Configure the DigitalOcean Provider
provider "digitalocean" {
  token = var.do_token
}
