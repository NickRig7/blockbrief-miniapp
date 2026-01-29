#!/bin/bash
set -e

echo "🚀 Deploying BlockBrief..."

# Check prerequisites
if ! command -v sam &> /dev/null; then
    echo "❌ AWS SAM CLI not found. Install: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Install Node.js: https://nodejs.org/"
    exit 1
fi

# Get Telegram Bot Token
read -p "Enter your Telegram Bot Token (from @BotFather): " BOT_TOKEN

if [ -z "$BOT_TOKEN" ]; then
    echo "❌ Bot token is required"
    exit 1
fi

# Deploy backend
echo "📦 Building backend..."
cd infrastructure
sam build

echo "🚀 Deploying backend to AWS..."
sam deploy \
    --guided \
    --parameter-overrides TelegramBotToken=$BOT_TOKEN \
    --capabilities CAPABILITY_IAM

# Get outputs
API_URL=$(aws cloudformation describe-stacks \
    --stack-name blockbrief \
    --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' \
    --output text)

FRONTEND_URL=$(aws cloudformation describe-stacks \
    --stack-name blockbrief \
    --query 'Stacks[0].Outputs[?OutputKey==`FrontendUrl`].OutputValue' \
    --output text)

WEBHOOK_URL=$(aws cloudformation describe-stacks \
    --stack-name blockbrief \
    --query 'Stacks[0].Outputs[?OutputKey==`WebhookUrl`].OutputValue' \
    --output text)

BUCKET_NAME=$(aws cloudformation describe-stacks \
    --stack-name blockbrief \
    --query 'Stacks[0].Outputs[?OutputKey==`FrontendBucket`].OutputValue' \
    --output text 2>/dev/null || echo "blockbrief-frontend-$(aws sts get-caller-identity --query Account --output text)")

echo "✅ Backend deployed!"
echo "API URL: $API_URL"

# Set Telegram webhook
echo "🔗 Setting Telegram webhook..."
curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" \
    -H "Content-Type: application/json" \
    -d "{\"url\": \"${WEBHOOK_URL}\"}"

# Build and deploy frontend
echo "📦 Building frontend..."
cd ../frontend

# Create .env file
echo "VITE_API_URL=$API_URL" > .env

# Install dependencies and build
npm install
npm run build

# Deploy to S3
echo "🚀 Deploying frontend to S3..."
aws s3 sync build/client s3://$BUCKET_NAME --delete

# Invalidate CloudFront cache
DISTRIBUTION_ID=$(aws cloudfront list-distributions \
    --query "DistributionList.Items[?Origins.Items[?DomainName=='${BUCKET_NAME}.s3.amazonaws.com']].Id" \
    --output text 2>/dev/null || echo "")

if [ ! -z "$DISTRIBUTION_ID" ]; then
    echo "🔄 Invalidating CloudFront cache..."
    aws cloudfront create-invalidation \
        --distribution-id $DISTRIBUTION_ID \
        --paths "/*"
fi

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📱 Next steps:"
echo "1. Open Telegram and find your bot"
echo "2. Send /start to register"
echo "3. Set Mini App URL in @BotFather:"
echo "   /setmenubutton -> select your bot -> send: https://$FRONTEND_URL"
echo ""
echo "🔗 URLs:"
echo "   Frontend: https://$FRONTEND_URL"
echo "   API: $API_URL"
echo ""
echo "⏰ The AI Editor will publish the first brief in ~6 hours"
echo "   Or trigger manually: aws stepfunctions start-execution --state-machine-arn <arn>"
