resource "aws_ssm_parameter" "control-environment-dev" {
  name = "foo-dev"
  type = "String"
  value = "development"
}

resource "aws_ssm_parameter" "control-environment-hom" {
  name = "foo-hom"
  type = "String"
  value = "homologation-v4"
}

################################################# TRUE INFRA ##################################################
module "ecr" {
  source = "./modules/ecr"
  name   = "repo-lambda-mlops"
}


module "iam-settings" {
  source = "./modules/iam"
  role_name = "role-lambda-mlops"
}

# module "lambda_v1" {
#   source = "../../modules/lambda"

#   function_name   = "hello-lambda"
#   lambda_role_arn = module.iam-settings.role_arn

#   image_uri = "${module.ecr.repository_url}:v1"

#   alias_name = "v0.0.0"
# }