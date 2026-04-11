variable "function_name" {
  type = string
}

variable "lambda_role_arn" {
  type = string
}

variable "image_uri" {
  type = string
}

variable "alias_name" {
  type = string
  default = null
}

variable "aliases" {
  type = map(object({
    version             = string
    additional_weights  = optional(map(number))
  }))
}