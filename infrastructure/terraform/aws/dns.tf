

# ssl cert
resource "aws_acm_certificate" "cert" {
  domain_name       = "scavenger.news"
  validation_method = "DNS"

  tags = {
    Environment = "development"
  }

  lifecycle {
    create_before_destroy = true
  }
}

# aws_route53_record
resource "aws_route53_record" "www" {
  zone_id = "Z02270332VCSNF4XI5BQW"
  name    = "scavenger.news"
  type    = "A"

  alias {
    name                   = aws_lb.scavenger.dns_name
    zone_id                = aws_lb.scavenger.zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "example" {
  for_each = {
    for dvo in aws_acm_certificate.cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = "Z02270332VCSNF4XI5BQW"
}

resource "aws_acm_certificate_validation" "example" {
  certificate_arn         = aws_acm_certificate.cert.arn
  validation_record_fqdns = [for record in aws_route53_record.example : record.fqdn]
}
