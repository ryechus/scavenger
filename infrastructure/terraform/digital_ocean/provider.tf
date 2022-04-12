terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
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
  default = "dop_v1_8e93ef76def94c241b8f1c7ad3fac48c200830ad2d98dd947434ae0af8c302c8"
}

# Configure the DigitalOcean Provider
provider "digitalocean" {
  token = var.do_token
}
