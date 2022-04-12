resource "aws_s3_bucket" "scavenger-django-storage" {
  bucket = "scavenger-django-storage"
}

resource "aws_s3_bucket_acl" "scavenger-django-storage-private" {
  bucket = aws_s3_bucket.scavenger-django-storage.id
  acl    = "private"
}

resource "aws_s3_bucket_cors_configuration" "example" {
  bucket = aws_s3_bucket.scavenger-django-storage.bucket

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}