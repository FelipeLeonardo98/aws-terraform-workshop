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
  for_each = var.aliases

  name             = each.key
  function_name    = aws_lambda_function.this.function_name
  function_version = each.value.version

  dynamic "routing_config" {
    for_each = each.value.additional_weights != null ? [1] : []

    content {
      additional_version_weights = each.value.additional_weights
    }
  }
  
  depends_on = [ aws_lambda_function.this ]
}