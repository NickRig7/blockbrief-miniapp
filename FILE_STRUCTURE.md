# BlockBrief - Project File Structure

```
blockbrief/
│
├── 📄 Documentation
│   ├── README.md                    # Project overview with diagrams
│   ├── QUICKSTART.md               # Step-by-step deployment guide
│   ├── ARCHITECTURE.md             # Detailed technical architecture
│   ├── DEMO_SCRIPT.md              # Hackathon presentation guide
│   ├── PROJECT_SUMMARY.md          # Comprehensive project summary
│   └── CHECKLIST.md                # Pre-deployment & demo checklist
│
├── 🚀 Deployment
│   └── deploy.sh                   # Automated deployment script
│
├── 🏗️ Infrastructure (AWS SAM)
│   └── infrastructure/
│       ├── template.yaml           # CloudFormation/SAM template
│       ├── workflow.asl.json       # Step Functions workflow definition
│       └── samconfig.toml          # SAM CLI configuration
│
├── ⚙️ Backend (Lambda Functions)
│   └── backend/
│       └── functions/
│           ├── fetcher.py          # Fetch news from APIs
│           ├── editor.py           # AI curation (Bedrock Claude)
│           ├── publisher.py        # Send briefs via Telegram
│           ├── telegram_webhook.py # Handle bot commands (/start)
│           ├── api.py              # Mini App REST API
│           └── requirements.txt    # Python dependencies
│
├── 🎨 Frontend (Telegram Mini App)
│   └── frontend/
│       ├── app/
│       │   ├── root.tsx           # Layout with Telegram styling
│       │   └── routes/
│       │       ├── _index.tsx     # Index route (redirects to home)
│       │       ├── home.tsx       # Display briefs
│       │       └── preferences.tsx # User settings
│       ├── package.json           # Node.js dependencies
│       ├── tsconfig.json          # TypeScript configuration
│       ├── react-router.config.ts # React Router v7 config
│       ├── index.html             # HTML entry point
│       └── .env.example           # Environment variables template
│
└── 🛠️ Scripts
    └── scripts/
        └── generate_demo_data.py   # Generate demo briefs for testing
```

## File Descriptions

### Documentation Files

**README.md**
- Project overview with visual diagrams
- Quick start instructions
- Architecture summary
- Cost breakdown

**QUICKSTART.md**
- Prerequisites checklist
- Step-by-step deployment guide
- Testing instructions
- Troubleshooting common issues
- Monitoring and logging commands

**ARCHITECTURE.md**
- Detailed system architecture diagrams
- Data flow explanations
- AI agent design (identity, tools, memory)
- AWS services breakdown
- Cost analysis
- Scalability considerations
- Security best practices

**DEMO_SCRIPT.md**
- Elevator pitch (30 seconds)
- Live demo flow (5 minutes)
- Key talking points
- Q&A preparation
- Winning differentiators
- Pre-demo checklist

**PROJECT_SUMMARY.md**
- Complete project overview
- Feature list (MVP + future)
- Metrics and performance
- Hackathon alignment
- Deployment summary

**CHECKLIST.md**
- Pre-deployment checklist
- Post-deployment testing
- Troubleshooting guide
- Demo day preparation

### Infrastructure Files

**infrastructure/template.yaml**
- SAM/CloudFormation template
- Defines all AWS resources:
  - 5 Lambda functions
  - 3 DynamoDB tables
  - Step Functions state machine
  - API Gateway
  - S3 bucket + CloudFront
  - IAM roles and policies
  - EventBridge schedule

**infrastructure/workflow.asl.json**
- Step Functions workflow definition
- 3-step process:
  1. Fetch news
  2. AI curation
  3. Publish to users

**infrastructure/samconfig.toml**
- SAM CLI configuration
- Default deployment parameters

### Backend Files

**backend/functions/fetcher.py**
- Fetches crypto news from CryptoCompare API
- Stores in DynamoDB with 24h TTL
- Triggered by Step Functions

**backend/functions/editor.py**
- Core AI agent logic
- Queries recent stories from DynamoDB
- Calls Amazon Bedrock (Claude 3.5 Sonnet):
  - Prompt 1: Select top 3-5 stories
  - Prompt 2: Write summaries
- Stores brief in DynamoDB

**backend/functions/publisher.py**
- Formats brief as HTML message
- Queries all users from DynamoDB
- Sends via Telegram Bot API

**backend/functions/telegram_webhook.py**
- Handles Telegram bot webhooks
- Processes /start command
- Registers new users in DynamoDB

**backend/functions/api.py**
- REST API for Mini App
- Endpoints:
  - GET /briefs - Fetch recent briefs
  - GET /preferences - Get user preferences
  - POST /preferences - Update preferences
- CORS-enabled

**backend/functions/requirements.txt**
- boto3 (AWS SDK)
- requests (HTTP client)

### Frontend Files

**frontend/app/root.tsx**
- Root layout component
- Telegram WebApp SDK initialization
- Global styles (Telegram theming)
- Navigation component

**frontend/app/routes/home.tsx**
- Home page component
- Displays latest briefs
- Story cards with:
  - Title
  - AI-generated summary
  - Source attribution
  - Read more link
- Loading and empty states

**frontend/app/routes/preferences.tsx**
- User preferences page
- Topic toggles (DeFi, NFTs, regulation, etc.)
- Frequency selection
- Save button with API integration

**frontend/app/routes/_index.tsx**
- Index route (redirects to home)

**frontend/package.json**
- React Router v7 dependencies
- React 18
- TypeScript
- Build scripts

**frontend/tsconfig.json**
- TypeScript compiler configuration
- React JSX support
- ES2022 target

**frontend/react-router.config.ts**
- React Router v7 configuration
- SSR disabled (SPA mode)

**frontend/index.html**
- HTML entry point
- Telegram WebApp SDK script

**frontend/.env.example**
- Environment variables template
- API_URL placeholder

### Scripts

**scripts/generate_demo_data.py**
- Generates sample briefs for testing
- Populates DynamoDB with demo data
- Useful for hackathon demo

**deploy.sh**
- Automated deployment script
- Builds and deploys backend (SAM)
- Builds and deploys frontend (S3)
- Sets Telegram webhook
- Configures CloudFront
- Outputs URLs and next steps

## Key Technologies

### Frontend
- **React 18** - UI library
- **React Router v7** - Routing (framework mode)
- **TypeScript** - Type safety
- **Telegram WebApp SDK** - Mini App integration
- **Vite** - Build tool

### Backend
- **Python 3.12** - Lambda runtime
- **boto3** - AWS SDK
- **requests** - HTTP client

### Infrastructure
- **AWS Lambda** - Serverless compute
- **Amazon Bedrock** - AI (Claude 3.5 Sonnet)
- **DynamoDB** - NoSQL database
- **Step Functions** - Workflow orchestration
- **EventBridge** - Scheduling
- **API Gateway** - REST API
- **S3** - Static hosting
- **CloudFront** - CDN
- **SAM** - Infrastructure as Code

### Integration
- **Telegram Bot API** - Message delivery
- **CryptoCompare API** - News source

## Total Files: 20 core files

- 6 documentation files
- 1 deployment script
- 3 infrastructure files
- 6 backend files
- 7 frontend files
- 1 utility script

## Lines of Code (Approximate)

- Backend Python: ~600 lines
- Frontend TypeScript/TSX: ~800 lines
- Infrastructure YAML/JSON: ~400 lines
- Documentation Markdown: ~3000 lines
- **Total: ~4800 lines**

## Getting Started

1. Read `README.md` for overview
2. Follow `QUICKSTART.md` for deployment
3. Review `ARCHITECTURE.md` for technical details
4. Use `CHECKLIST.md` before demo
5. Practice with `DEMO_SCRIPT.md`

---

**Ready to deploy? Run `./deploy.sh` and follow the prompts!** 🚀
