resource "aws_ssm_parameter" "control-environment-dev" {
  name = "ssm-control-dev-environment"
  type = "String"
  value = "development"
}

resource "aws_ssm_parameter" "control-environment-hom" {
  name = "ssm-control-hom-environment"
  type = "String"
  value = "homologation"
}