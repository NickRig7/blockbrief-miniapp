# BlockBrief 📰

> **Your AI Editor-in-Chief for Crypto News**

BlockBrief is an autonomous AI-powered news curator that delivers the most important crypto stories directly to your Telegram. Built on AWS serverless infrastructure with Amazon Bedrock.

```
┌─────────────────────────────────────────────────────────────┐
│  🌐 Crypto News Sources (20+ articles every 6 hours)       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  🤖 AI Editor-in-Chief (Amazon Bedrock - Claude 3.5)       │
│     • Analyzes all stories                                  │
│     • Scores importance (market impact, regulation, etc.)   │
│     • Selects top 3-5 stories                               │
│     • Writes concise summaries (60-80 words)                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  📱 Telegram Mini App                                       │
│     • Beautiful, responsive UI                              │
│     • Instant access (no install)                           │
│     • Personalized preferences                              │
│     • Brief history                                         │
└─────────────────────────────────────────────────────────────┘
```

## ✨ Features

- 🤖 **Autonomous AI Curation** - Claude 3.5 Sonnet selects and summarizes stories
- 📱 **Telegram Mini App** - Modern React UI, no installation required
- ⚡ **Real-time Delivery** - New briefs every 6 hours
- 🎯 **Personalized** - Choose topics (DeFi, NFTs, regulation, etc.)
- 💰 **Cost-Efficient** - $50/month for 1000 users
- 🚀 **Serverless** - Auto-scales on AWS Lambda, DynamoDB, Step Functions

## 🎯 Why BlockBrief?

**The Problem**: Crypto enthusiasts face information overload - hundreds of articles daily, duplicate stories, clickbait headlines.

**The Solution**: An AI Editor-in-Chief that autonomously curates news, filtering signal from noise, and delivers only what matters.

## Quick Start

### Prerequisites
- AWS Account with Bedrock access (us-east-1)
- Telegram Bot Token (from @BotFather)
- Node.js 18+
- Python 3.12+
- AWS SAM CLI

### Setup

1. **Configure Telegram Bot**
```bash
# Talk to @BotFather on Telegram
# /newbot -> follow prompts -> save token
```

2. **Deploy Backend**
```bash
cd infrastructure
sam build
sam deploy --guided
# Enter your Telegram bot token when prompted
```

3. **Deploy Frontend**
```bash
cd frontend
npm install
npm run build
# Deploy to S3/CloudFront (automated in SAM template)
```

4. **Set Telegram Mini App URL**
```bash
# In @BotFather:
# /setmenubutton -> select bot -> send URL from CloudFront
```

## Architecture

```
┌──────────────┐
│   Telegram   │  Users interact via Mini App & Bot
│    Users     │
└──────┬───────┘
       │
       ├─────────────────┐
       │                 │
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│ CloudFront  │   │ API Gateway │
│  + S3       │   │  + Lambda   │
│ (Mini App)  │   │  (Bot API)  │
└──────┬──────┘   └──────┬──────┘
       │                 │
       └────────┬────────┘
                │
                ▼
       ┌────────────────┐
       │  DynamoDB      │  ← User data, briefs, news cache
       └────────────────┘
                ▲
                │
       ┌────────┴────────┐
       │                 │
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│EventBridge  │   │    Step     │
│ (Schedule)  │──▶│  Functions  │  AI Workflow (every 6h)
└─────────────┘   └──────┬──────┘
                         │
                         ▼
                  ┌──────────────┐
                  │   Lambda     │
                  │  Functions   │
                  │ • Fetcher    │
                  │ • Editor     │──▶ Amazon Bedrock
                  │ • Publisher  │    (Claude 3.5)
                  └──────────────┘
```

**Tech Stack:**
- Frontend: React Router v7, TypeScript
- Backend: Python 3.12, AWS Lambda
- AI: Amazon Bedrock (Claude 3.5 Sonnet)
- Storage: DynamoDB, S3
- Orchestration: Step Functions, EventBridge
- Delivery: Telegram Bot API

## Cost

~$50/month for 1000 users
