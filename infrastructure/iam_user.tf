/*
resource "aws_iam_user" "django" {
  name = "django"
}

resource "aws_iam_access_key" "django" {
  user = aws_iam_user.django.name
}

resource "aws_iam_user_policy" "django_s3" {
  name = "test"
  user = aws_iam_user.django.name

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:PutObject",
        "s3:GetObjectAcl",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:DeleteObject",
        "s3:PutObjectAcl"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}
*/
