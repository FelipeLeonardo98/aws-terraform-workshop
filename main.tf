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

resource "aws_ssm_parameter" "control-environment-prod" {
  name = "foo-prod"
  type = "String"
  value = "production"
}

data "aws_s3_bucket" "tfstate_bucket" {
  bucket = "474668425182-github-oidc-terraform-tfstate"
}

module "lambda_2" {
  source = "./module"
  
}