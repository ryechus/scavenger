variable "source_code_version" {
  default = "e844e5720f6bf8c29cef3cac329098a8aa646498"
}

variable "aws_profile" {
  default = "zilla"
}

locals {
  aws_s3_url = "https://${data.aws_s3_bucket.scavenger-django-storage.bucket_domain_name}"
}