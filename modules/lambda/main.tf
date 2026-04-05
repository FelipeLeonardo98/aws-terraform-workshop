resource "aws_lambda_function" "this" {
  function_name = var.function_name
  role          = var.lambda_role_arn
  package_type  = "Image"
  image_uri     = var.image_uri

  publish = true

  #timeout = 10
  memory_size = 500
}

resource "aws_lambda_alias" "this" {
  name             = var.alias_name
  function_name    = aws_lambda_function.this.function_name
  function_version = aws_lambda_function.this.version
  depends_on = [ aws_lambda_function.this ]
}