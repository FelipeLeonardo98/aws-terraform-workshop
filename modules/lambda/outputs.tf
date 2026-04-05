output "function_name" {
  value = aws_lambda_function.this.function_name
}

output "version" {
  value = aws_lambda_function.this.version
}

output "alias_arn" {
  value = aws_lambda_alias.this.arn
}