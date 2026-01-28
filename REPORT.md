<!--
	#
	#	Hi!
	#	Press Ctrl+Shift+V to open this report in Preview Mode
	#
-->

# Miniapp "tma-blockbrief" Deployment Report

## Quick Start

Configure your Miniapp and/or bot's Menu button with [@BotFather](https://t.me/botfather) using:

**Miniapp URL:** [https://d2v2tke97m376i.cloudfront.net/app](https://d2v2tke97m376i.cloudfront.net/app)



**Deployed to regions:**

- Main: **us-east-1**
- Global: **us-east-1**

## Code Repository

Clone your repository, update application code and push it to origin for automatic deployment in the cloud.



Setup [credentials helper](https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-https-unixes.html) to allow git authenticate to your CodeCommit repository:

~~~bash
# Configure credentials helper
git config --global credential.helper '!aws codecommit credential-helper $@'
git config --global credential.UseHttpPath true

# Clone repository
git clone https://git-codecommit.us-east-1.amazonaws.com/v1/repos/tma-blockbrief
~~~

## Redeploy Changes

To publish updates to the cloud:



~~~bash
# 1. Commit your changes
git add .
git commit -m "Your update description"

# 2. Push to main branch to trigger build
git push origin main
~~~



The build script from **codebuild.yaml** will run automatically on push to **main**.

## Monitoring & Logs

### CloudWatch Logs

- **Application Logs:** [View logs](https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/tma-blockbrief)
-   - Lambda execution logs
-   - SSR request/response logs
-   - Retention: 6 months
- **Build Logs:** [View logs](https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/tma-blockbrief-build)
-   - CodeBuild execution logs
-   - Deployment history
-   - Retention: 6 months



### Useful Commands

~~~bash
# Tail application logs
aws logs tail https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/tma-blockbrief --follow --region us-east-1

# Tail build project logs
aws logs tail https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/tma-blockbrief-build --follow --region us-east-1

# View recent errors
aws logs filter-log-events \
  --log-group-name https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/tma-blockbrief \
  --filter-pattern "ERROR" \
  --region us-east-1
~~~

## Resource ARNs & Console Links

### Lambda Function

- **Name:** `tma-blockbrief-backend`
- **ARN:** `arn:aws:lambda:us-east-1:524184902791:function:tma-blockbrief-backend`
- [Open in Console](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions)



### CloudFront Distribution

- **ID:** `E1D8PJA9GN1NCI`
- **Domain:** [d2v2tke97m376i.cloudfront.net](https://d2v2tke97m376i.cloudfront.net)
- [Open in Console](https://console.aws.amazon.com/cloudfront/v4/home#/distributions/E1D8PJA9GN1NCI)



### S3 Bucket

- **Name:** `tma-blockbrief-web-static-content-45b5f5bfec79faec107f4a8205ded`
- **ARN:** `arn:aws:s3:::tma-blockbrief-web-static-content-45b5f5bfec79faec107f4a8205ded`
- [Open in Console](https://us-east-1.console.aws.amazon.com/s3/buckets?region=us-east-1)



### CodeCommit Repository

- **Name:** `tma-blockbrief`
- **ARN:** `arn:aws:codecommit:us-east-1:524184902791:tma-blockbrief`
- [Open in Console](https://us-east-1.console.aws.amazon.com/codesuite/codecommit/repositories?region=us-east-1)



### Stack Information

- **Main Stack:** `arn:aws:cloudformation:us-east-1:524184902791:stack/tma-blockbrief/4abaf960-fc0c-11f0-b8d1-124806eb9387`
- **Global Stack:** `arn:aws:cloudformation:us-east-1:524184902791:stack/tma-blockbrief/4abaf960-fc0c-11f0-b8d1-124806eb9387`
- [Open CloudFormation](https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks)

## Database Tables

Your application uses **3** DynamoDB tables:



| Table Name | Partition Key | Sort Key | TTL | Purpose |
| --- | --- | --- | --- | --- |
| `tma-blockbrief-config` | tenant | id | - | Application configuration storage |
| `tma-blockbrief-users` | id | order (N) | - | User data and profiles |
| `tma-blockbrief-sessions` | user | session | ✓ (ttl) | User sessions (90-day TTL) |



[DynamoDB Console](https://us-east-1.console.aws.amazon.com/dynamodbv2/home?region=us-east-1#tables)

## Lambda Configuration

Your application backend runs on AWS Lambda with the following configuration:



| Property | Value |
| --- | --- |
| Runtime | Node.js 22.x |
| Architecture | ARM64 |
| Memory Size | 256 MB |
| Timeout | 30 seconds |
| Base Path | `/app` |
| Health Check | `/app/ok` |
| Port | 7000 |



[Lambda Console](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions)

## AI/Bedrock Configuration

Your application is configured to use Amazon Bedrock with the following settings:



- **Model:** `us.anthropic.claude-sonnet-4-5-20250929-v1:0`
- **Region:** **us-east-1**
- **Max Tokens:** 10240
- **Top-P:** 0.9
- **Guardrail:** `td5cc6fpdgxc` (version DRAFT)



> ℹ️ **INFO**: Guardrail provides content filtering for: Sexual, Violence, Hate, Insults, Misconduct, and Prompt Attack



[Bedrock Console](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/guardrails)

## Security Configuration

### Session Management

- **Session TTL:** 90 days
- **Cookie Name:** `SESSION`
- **Cookie Max Age:** 4 hours
- **Telegram Auth Tolerance:** 5 minutes



### Telegram Webhook

- **Webhook Path:** `/app/bot`
- **Firewall:** **cff**
- **Rate Limit:** 50 requests/second within 5 minutes interval



### CDN & WAF

- **WAF Enabled:** ✓ Yes
- **Geo-blocking:** IQ, IR, KP, CN



> ℹ️ **INFO**: WAF provides protection against common web exploits and can block traffic from specific geographic regions

## Bot Webhook

Your webhook should already be configured. No action required.



If you need to manually set the webhook:

**Bot Webhook URL:** [https://d4qauiwgttjqv.cloudfront.net/app/bot](https://d4qauiwgttjqv.cloudfront.net/app/bot)



> ℹ️ **INFO**: The webhook is automatically configured during deployment

## Next Steps

Complete your deployment by following these steps:



- ☐ Test miniapp in Telegram: [Open miniapp](https://d2v2tke97m376i.cloudfront.net/app)
- ☐ Review CloudWatch logs to verify everything is working: [View logs](https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/tma-blockbrief)
- ☐ Clone the repository and make your first commit
- ☐ Set up monitoring alerts in CloudWatch (optional)
- ☐ Configure custom domain for CloudFront distribution (optional)
- ☐ Review security settings and adjust as needed



> ℹ️ **INFO**: All resources are deployed and ready. Start by testing your miniapp in Telegram!