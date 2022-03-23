resource "aws_s3_bucket" "scavenger-django-storage" {
  bucket = "scavenger-django-storage"
}

resource "aws_s3_bucket_acl" "scavenger-django-storage-private" {
  bucket = aws_s3_bucket.scavenger-django-storage.id
  acl    = "private"
}