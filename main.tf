resource "aws_ssm_parameter" "control-environment-dev" {
  name = "foo-dev"
  type = "String"
  value = "development"
}

resource "aws_ssm_parameter" "control-environment-hom" {
  name = "foo-hom"
  type = "String"
  value = "homologation"
}