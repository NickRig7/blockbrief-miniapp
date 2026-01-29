# BlockBrief - Pre-Deployment Checklist

## ✅ Project Files

### Documentation
- [x] README.md - Project overview with visual diagrams
- [x] QUICKSTART.md - Deployment guide
- [x] ARCHITECTURE.md - Detailed technical architecture
- [x] DEMO_SCRIPT.md - Hackathon presentation guide
- [x] PROJECT_SUMMARY.md - Comprehensive summary

### Infrastructure
- [x] infrastructure/template.yaml - SAM/CloudFormation template
- [x] infrastructure/workflow.asl.json - Step Functions workflow
- [x] infrastructure/samconfig.toml - SAM configuration
- [x] deploy.sh - Automated deployment script

### Backend (Lambda Functions)
- [x] backend/functions/fetcher.py - News fetching
- [x] backend/functions/editor.py - AI curation with Bedrock
- [x] backend/functions/publisher.py - Telegram delivery
- [x] backend/functions/telegram_webhook.py - Bot commands
- [x] backend/functions/api.py - Mini App API
- [x] backend/functions/requirements.txt - Dependencies

### Frontend (React Router v7)
- [x] frontend/app/root.tsx - Layout with Telegram styling
- [x] frontend/app/routes/_index.tsx - Index route
- [x] frontend/app/routes/home.tsx - Briefs display
- [x] frontend/app/routes/preferences.tsx - User settings
- [x] frontend/package.json - Dependencies
- [x] frontend/tsconfig.json - TypeScript config
- [x] frontend/react-router.config.ts - React Router config
- [x] frontend/.env.example - Environment variables template

### Scripts
- [x] scripts/generate_demo_data.py - Demo data generator

## 🚀 Pre-Deployment Steps

### 1. AWS Prerequisites
- [ ] AWS Account created
- [ ] AWS CLI installed and configured (`aws configure`)
- [ ] AWS SAM CLI installed
- [ ] Bedrock access enabled in us-east-1
- [ ] Claude 3.5 Sonnet model enabled in Bedrock console

### 2. Telegram Prerequisites
- [ ] Telegram account created
- [ ] Bot created via @BotFather
- [ ] Bot token saved securely
- [ ] Bot username noted

### 3. Local Prerequisites
- [ ] Node.js 18+ installed
- [ ] Python 3.12+ installed
- [ ] Git installed (optional, for version control)

## 📋 Deployment Checklist

### Automated Deployment
```bash
cd blockbrief
./deploy.sh
# Follow prompts
```

### Manual Deployment Steps
- [ ] 1. Build backend: `cd infrastructure && sam build`
- [ ] 2. Deploy backend: `sam deploy --guided`
- [ ] 3. Note API Gateway URL from outputs
- [ ] 4. Create frontend .env: `echo "VITE_API_URL=<api-url>" > frontend/.env`
- [ ] 5. Install frontend deps: `cd frontend && npm install`
- [ ] 6. Build frontend: `npm run build`
- [ ] 7. Get S3 bucket name from CloudFormation outputs
- [ ] 8. Deploy frontend: `aws s3 sync build/client s3://<bucket-name>`
- [ ] 9. Get CloudFront URL from outputs
- [ ] 10. Set Telegram webhook: `curl -X POST https://api.telegram.org/bot<TOKEN>/setWebhook -d url=<webhook-url>`
- [ ] 11. Configure Mini App in @BotFather: `/setmenubutton`

## 🧪 Post-Deployment Testing

### 1. Test Backend
- [ ] Check CloudFormation stack status: `aws cloudformation describe-stacks --stack-name blockbrief`
- [ ] Verify Lambda functions exist: `aws lambda list-functions | grep blockbrief`
- [ ] Check DynamoDB tables: `aws dynamodb list-tables | grep blockbrief`
- [ ] View Step Functions: AWS Console → Step Functions

### 2. Test Telegram Bot
- [ ] Open Telegram, search for your bot
- [ ] Send `/start` command
- [ ] Verify user registered in DynamoDB: `aws dynamodb scan --table-name blockbrief-users`
- [ ] Check webhook status: `curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo`

### 3. Test Mini App
- [ ] Open bot in Telegram
- [ ] Tap menu button (should open Mini App)
- [ ] Verify CloudFront URL loads
- [ ] Check browser console for errors
- [ ] Test navigation (Home ↔ Settings)

### 4. Test AI Workflow
- [ ] Generate demo data: `python scripts/generate_demo_data.py`
- [ ] Verify briefs in DynamoDB: `aws dynamodb scan --table-name blockbrief-briefs`
- [ ] Refresh Mini App, verify briefs display
- [ ] Manually trigger workflow: `aws stepfunctions start-execution --state-machine-arn <arn>`
- [ ] Monitor execution: AWS Console → Step Functions → Executions
- [ ] Check CloudWatch logs for errors

### 5. Test User Preferences
- [ ] Open Settings in Mini App
- [ ] Toggle topics
- [ ] Change frequency
- [ ] Tap "Save Preferences"
- [ ] Verify saved in DynamoDB: `aws dynamodb get-item --table-name blockbrief-users --key '{"userId":{"S":"<your-user-id>"}}'`

## 🐛 Troubleshooting

### Common Issues

**Issue**: "AccessDeniedException" from Bedrock
- **Fix**: Enable Claude 3.5 Sonnet in Bedrock console (us-east-1)
- **Check**: IAM role for Lambda has `bedrock:InvokeModel` permission

**Issue**: Mini App not loading
- **Fix**: Wait 15 minutes for CloudFront distribution to deploy
- **Check**: `aws cloudfront list-distributions`
- **Check**: S3 bucket has files: `aws s3 ls s3://<bucket-name>`

**Issue**: No briefs appearing
- **Fix**: Run demo data script: `python scripts/generate_demo_data.py`
- **Check**: DynamoDB table: `aws dynamodb scan --table-name blockbrief-briefs`

**Issue**: Telegram webhook not working
- **Fix**: Verify webhook URL is correct
- **Check**: `curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo`
- **Fix**: Re-set webhook with correct URL

**Issue**: Lambda timeout
- **Fix**: Increase timeout in template.yaml (default: 60s)
- **Check**: CloudWatch logs for specific error

**Issue**: CORS errors in browser
- **Fix**: Verify API Gateway CORS configuration in template.yaml
- **Check**: Browser network tab for preflight requests

## 📊 Monitoring

### CloudWatch Logs
```bash
# View all logs
sam logs --stack-name blockbrief --tail

# Specific function
aws logs tail /aws/lambda/blockbrief-EditorFunction-XXXXX --follow
```

### DynamoDB Data
```bash
# View users
aws dynamodb scan --table-name blockbrief-users

# View briefs
aws dynamodb scan --table-name blockbrief-briefs

# View news cache
aws dynamodb scan --table-name blockbrief-news --limit 5
```

### Step Functions
- AWS Console → Step Functions → State machines
- Click on "blockbrief-EditorStateMachine"
- View executions and logs

## 🎯 Hackathon Demo Prep

### Day Before
- [ ] Deploy to AWS
- [ ] Generate demo data
- [ ] Test all features
- [ ] Prepare screenshots (backup)
- [ ] Record demo video (backup)
- [ ] Charge phone and laptop
- [ ] Test screen sharing

### Demo Day
- [ ] Open AWS Console tabs:
  - [ ] Step Functions
  - [ ] Lambda
  - [ ] DynamoDB
  - [ ] CloudWatch Logs
- [ ] Open Telegram on phone
- [ ] Open Mini App (verify it loads)
- [ ] Have architecture diagram ready
- [ ] Have cost breakdown ready
- [ ] Review Q&A in DEMO_SCRIPT.md

## 📚 Resources

- [AWS SAM CLI Installation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- [Amazon Bedrock Getting Started](https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- [React Router v7](https://reactrouter.com/)

## 🆘 Support

If you encounter issues:
1. Check CloudWatch Logs for errors
2. Verify DynamoDB tables have data
3. Check Step Functions execution history
4. Verify Telegram webhook status
5. Review QUICKSTART.md troubleshooting section

## ✅ Final Verification

Before demo:
- [ ] Mini App loads on phone
- [ ] Briefs display correctly
- [ ] Preferences save successfully
- [ ] Bot responds to /start
- [ ] Step Functions workflow completes
- [ ] No errors in CloudWatch Logs
- [ ] Cost estimate is accurate
- [ ] Demo script reviewed

---

**You're ready to win the hackathon! 🚀**
