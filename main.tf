resource "aws_ssm_parameter" "control-environment" {
  name = "ssm-control-environment"
  type = "String"
  value = "development"
}