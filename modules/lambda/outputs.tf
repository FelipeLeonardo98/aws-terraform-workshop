output "function_name" {
  value = aws_lambda_function.this.function_name
}

output "version" {
  value = aws_lambda_function.this.version
}

output "alias_arns" {
  value = {
    for alias_name, alias_resource in aws_lambda_alias.this :
    alias_name => alias_resource.arn
  }
}

output "alias_versions" {
  value = {
    for alias_name, alias_resource in aws_lambda_alias.this :
    alias_name => alias_resource.function_version
  }
}