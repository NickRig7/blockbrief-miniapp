# BlockBrief - Quick Start Guide

## 🎯 What You're Building

An AI-powered crypto news curator that:
- Fetches news from multiple sources every 6 hours
- Uses Amazon Bedrock (Claude) to select the top 3-5 stories
- Generates concise summaries
- Delivers via Telegram Mini App
- Fully serverless on AWS

## 📋 Prerequisites

1. **AWS Account** with Bedrock access in us-east-1
   - Enable Claude 3.5 Sonnet model in Bedrock console
   
2. **Telegram Bot**
   - Open Telegram, search for @BotFather
   - Send `/newbot` and follow prompts
   - Save your bot token

3. **Local Tools**
   - AWS CLI configured (`aws configure`)
   - AWS SAM CLI ([install guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html))
   - Node.js 18+ and npm
   - Python 3.12+

## 🚀 Deployment (5 minutes)

### Option 1: Automated Deployment

```bash
cd blockbrief
./deploy.sh
# Enter your Telegram bot token when prompted
```

### Option 2: Manual Deployment

```bash
# 1. Deploy backend
cd infrastructure
sam build
sam deploy --guided \
    --parameter-overrides TelegramBotToken=YOUR_BOT_TOKEN \
    --capabilities CAPABILITY_IAM

# 2. Get API URL from outputs
export API_URL=$(aws cloudformation describe-stacks \
    --stack-name blockbrief \
    --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' \
    --output text)

# 3. Build frontend
cd ../frontend
echo "VITE_API_URL=$API_URL" > .env
npm install
npm run build

# 4. Deploy frontend to S3
export BUCKET=$(aws cloudformation describe-stacks \
    --stack-name blockbrief \
    --query 'Stacks[0].Outputs[?OutputKey==`FrontendBucket`].OutputValue' \
    --output text)
aws s3 sync build/client s3://$BUCKET

# 5. Get CloudFront URL
export FRONTEND_URL=$(aws cloudformation describe-stacks \
    --stack-name blockbrief \
    --query 'Stacks[0].Outputs[?OutputKey==`FrontendUrl`].OutputValue' \
    --output text)

echo "Frontend URL: https://$FRONTEND_URL"
```

## 📱 Configure Telegram Mini App

1. Open Telegram, find @BotFather
2. Send `/setmenubutton`
3. Select your bot
4. Send the CloudFront URL from deployment output
5. Test: Open your bot, tap the menu button

## 🧪 Testing

### Test the AI Editor Manually

```bash
# Trigger the workflow immediately (don't wait 6 hours)
STATE_MACHINE_ARN=$(aws cloudformation describe-stacks \
    --stack-name blockbrief \
    --query 'Stacks[0].Outputs[?OutputKey==`EditorStateMachineArn`].OutputValue' \
    --output text)

aws stepfunctions start-execution \
    --state-machine-arn $STATE_MACHINE_ARN
```

### Test Individual Functions

```bash
# Test news fetcher
aws lambda invoke \
    --function-name blockbrief-FetcherFunction-XXXXX \
    --payload '{}' \
    response.json

# Test AI editor
aws lambda invoke \
    --function-name blockbrief-EditorFunction-XXXXX \
    --payload '{"action":"curate"}' \
    response.json
```

### Check DynamoDB Tables

```bash
# View fetched news
aws dynamodb scan --table-name blockbrief-news --limit 5

# View published briefs
aws dynamodb scan --table-name blockbrief-briefs --limit 5

# View users
aws dynamodb scan --table-name blockbrief-users
```

## 🎨 Customization

### Change AI Behavior

Edit `backend/functions/editor.py`:
- Modify `EDITOR_PROMPT` to change selection criteria
- Modify `WRITER_PROMPT` to change summary style
- Adjust `max_tokens` for longer/shorter summaries

### Change Schedule

Edit `infrastructure/template.yaml`:
```yaml
Schedule: rate(6 hours)  # Change to rate(3 hours), rate(12 hours), etc.
```

### Add News Sources

Edit `backend/functions/fetcher.py`:
```python
NEWS_SOURCES = [
    # Add your API endpoints here
    {'name': 'YourSource', 'url': 'https://...', 'type': 'api'}
]
```

### Customize UI

Edit `frontend/app/root.tsx` for styling
Edit `frontend/app/routes/home.tsx` for layout

## 💰 Cost Optimization

**Current costs (~$50/month for 1000 users):**
- Lambda: $5
- DynamoDB: $10
- Bedrock: $30
- S3 + CloudFront: $5

**To reduce costs:**

1. **Reduce Bedrock usage:**
```python
# Cache AI responses in DynamoDB
# Only re-analyze if story changed
```

2. **Use Lambda reserved concurrency:**
```yaml
ReservedConcurrentExecutions: 1  # Prevent over-scaling
```

3. **Optimize DynamoDB:**
```yaml
BillingMode: PROVISIONED  # If traffic is predictable
ReadCapacityUnits: 5
WriteCapacityUnits: 5
```

## 🐛 Troubleshooting

### "AccessDeniedException" from Bedrock
- Enable Claude 3.5 Sonnet in Bedrock console (us-east-1)
- Check IAM permissions for Lambda execution role

### No briefs appearing
- Check Step Functions execution: AWS Console → Step Functions
- Check Lambda logs: AWS Console → CloudWatch Logs
- Manually trigger: `aws stepfunctions start-execution --state-machine-arn <arn>`

### Telegram webhook not working
- Verify webhook URL: `curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo`
- Check API Gateway logs in CloudWatch

### Frontend not loading
- Check CloudFront distribution status (takes ~15 min to deploy)
- Verify S3 bucket has files: `aws s3 ls s3://blockbrief-frontend-<account-id>`
- Check browser console for API errors

## 📊 Monitoring

### View Logs
```bash
# Lambda logs
sam logs --stack-name blockbrief --tail

# Specific function
aws logs tail /aws/lambda/blockbrief-EditorFunction-XXXXX --follow
```

### Check Metrics
```bash
# Lambda invocations
aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Invocations \
    --dimensions Name=FunctionName,Value=blockbrief-EditorFunction-XXXXX \
    --start-time 2024-01-01T00:00:00Z \
    --end-time 2024-01-02T00:00:00Z \
    --period 3600 \
    --statistics Sum
```

## 🎯 Hackathon Demo Tips

1. **Pre-populate data:** Run the workflow 2-3 times before demo
2. **Show AI in action:** Display Bedrock prompts and responses
3. **Highlight serverless:** Show AWS console with Lambda, Step Functions
4. **User experience:** Demo on actual Telegram app (not web)
5. **Cost efficiency:** Show cost breakdown and optimization strategies

## 🚀 Next Steps

### MVP Enhancements
- [ ] Add user engagement tracking (clicks, reads)
- [ ] Implement topic-based filtering
- [ ] Add push notifications for breaking news
- [ ] Create admin dashboard

### Advanced Features
- [ ] Multi-language support
- [ ] Sentiment analysis
- [ ] Price alerts integration
- [ ] Social sharing

## 📚 Resources

- [Telegram Mini Apps Docs](https://core.telegram.org/bots/webapps)
- [Amazon Bedrock Docs](https://docs.aws.amazon.com/bedrock/)
- [React Router v7 Docs](https://reactrouter.com/)
- [AWS SAM Docs](https://docs.aws.amazon.com/serverless-application-model/)

## 🆘 Support

Issues? Check:
1. CloudWatch Logs for errors
2. DynamoDB tables for data
3. Step Functions execution history
4. Telegram webhook status

Good luck with your hackathon! 🚀
