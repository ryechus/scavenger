# load balancer
resource "aws_lb" "scavenger" {
  name               = "scavenger-lb-dev"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.allow_tls.id]
  subnets            = ["subnet-28a2344e", "subnet-a8d173f2"]

  enable_deletion_protection = true

#  access_logs {
#    bucket  = aws_s3_bucket.logs.bucket
#    prefix  = "scavenger-lb"
#    enabled = true
#  }

  tags = {
    Environment = "development"
  }
}

 # load balancer listener
resource "aws_lb_listener" "front_end" {
  load_balancer_arn = aws_lb.scavenger.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = aws_acm_certificate_validation.example.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.cms.arn
  }
}

resource "aws_lb_listener" "front_end_forward" {
  load_balancer_arn = aws_lb.scavenger.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

# target group
resource "aws_lb_target_group" "cms" {
  port     = 8000
  protocol = "HTTP"
  vpc_id   = data.aws_vpc.main.id
  target_type = "ip"

  tags = {
    Environment = "development"
  }
}
