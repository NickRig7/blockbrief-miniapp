# BlockBrief 📰

> **Your AI Editor-in-Chief for Crypto News**

BlockBrief is an autonomous AI-powered news curator that delivers the most important crypto stories directly to your Telegram. Built on AWS serverless infrastructure with Amazon Bedrock.

## ✨ Features

- 🤖 **Autonomous AI Curation** - Claude 3.5 Sonnet selects and summarizes stories
- 📱 **Telegram Mini App** - Modern UI with Telegram design system
- ⚡ **Real-time Updates** - Latest crypto news from multiple sources
- 🔖 **Save Articles** - Bookmark stories to read later
- 🔍 **Search & Filter** - Find news by category or keyword
- 💰 **Cost-Efficient** - Serverless architecture on AWS
- 🚀 **Auto-Scaling** - Handles any load with Lambda & DynamoDB

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
```

3. **Set Bot Menu Button**
```bash
# In @BotFather:
# /mybots -> select bot -> Bot Settings -> Menu Button
# Enter your Mini App URL
```

## Architecture

**Tech Stack:**
- Frontend: HTML5, Vanilla JavaScript, Telegram Web App SDK
- Backend: Python 3.12, AWS Lambda, Grammy (Telegram Bot Framework)
- AI: Amazon Bedrock (Claude 3.5 Sonnet)
- Storage: DynamoDB, S3
- Orchestration: Step Functions, EventBridge
- Delivery: Telegram Bot API

## Project Structure

```
blockbrief/
├── bot/                    # Telegram bot (Grammy framework)
├── core/                   # Shared utilities
├── backend/functions/      # Lambda functions
├── infrastructure/         # SAM templates
├── blockbrief-miniapp/     # Mini App (deployed to GitHub Pages)
└── UIKit/                  # Telegram design system
```

## Mini App

The Mini App is a standalone HTML application that provides:
- 📰 News feed with categories (All, Bitcoin, Crypto, Insights, Stocks)
- 🔖 Save articles for later
- 🔍 Search functionality
- 📱 Telegram design system with smooth animations
- 🎨 Native Telegram theme support

Deployed at: https://nickrig7.github.io/blockbrief-miniapp/

## Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## License

See LICENSE file for details.
