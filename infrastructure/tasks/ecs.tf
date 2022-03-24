# ecs service
resource "aws_ecs_service" "scavenger" {
  name                       = "scavenger-bblog"
  cluster                    = data.aws_ecs_cluster.scavenger.id
  task_definition            = aws_ecs_task_definition.scavenger.arn
  desired_count              = 1
  deployment_maximum_percent = 200
  launch_type                = "FARGATE"
  network_configuration {
    subnets          = ["subnet-28a2344e", "subnet-a8d173f2"]
    assign_public_ip = true
  }
  load_balancer {
    target_group_arn = data.aws_lb_target_group.cms.arn
    container_name   = "scavenger"
    container_port   = 8000
  }
}