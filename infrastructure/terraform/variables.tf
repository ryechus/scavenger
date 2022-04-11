variable "source_code_version" {
  default = "5164bb18b74e1ea05eac860cd8c477c4cc10d697"
}

variable "env" {
  default = "dev"
}

variable "env_instance" {
  default = ""
}

variable "aws_profile" {
  default = "zilla"
}

locals {
  env = "${var.env}${var.env_instance}"
}