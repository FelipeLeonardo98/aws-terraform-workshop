terraform {
    backend "s3" {
      bucket = "474668425182-github-oidc-terraform-tfstate"
      key = "infra.tfstate"
      region = "us-east-1"
    }
}