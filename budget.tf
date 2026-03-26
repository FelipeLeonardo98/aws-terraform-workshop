
resource "aws_budgets_budget" "monthly_budget" {
  name              = "budget-example"
  budget_type       = "COST"
  limit_amount      = 10
  limit_unit        = "USD"
  time_unit         = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 50
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = ["felipeferrazleonardo98@gmail.com"]
  }
}