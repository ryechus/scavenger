variable "source_code_version" {
  default = "5164bb18b74e1ea05eac860cd8c477c4cc10d697"
}

variable "aws_profile" {
  default = "zilla"
}

locals {
  aws_s3_url = "https://${data.aws_s3_bucket.scavenger-django-storage.bucket_domain_name}"
}