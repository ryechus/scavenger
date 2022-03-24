variable "source_code_version" {
  default = "80cf1ea3bc8d25e19da3f75f5bcb1f41c337582b"
}

variable "aws_profile" {
  default = "zilla"
}

locals {
  aws_s3_url = "https://${data.aws_s3_bucket.scavenger-django-storage.bucket_domain_name}"
}