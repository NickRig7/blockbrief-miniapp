# BlockBrief Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         TELEGRAM USERS                          │
│                    (Mini App + Bot Messages)                    │
└────────────┬────────────────────────────────┬───────────────────┘
             │                                │
             │ Mini App                       │ Bot Commands
             │ (HTTPS)                        │ (Webhook)
             ▼                                ▼
┌────────────────────────┐      ┌────────────────────────────────┐
│   CloudFront + S3      │      │      API Gateway               │
│   (React Router v7)    │      │      /webhook                  │
│   - Home (Briefs)      │      │      /briefs                   │
│   - Preferences        │      │      /preferences              │
└────────────┬───────────┘      └────────────┬───────────────────┘
             │                                │
             │ API Calls                      │ Invoke
             ▼                                ▼
┌────────────────────────────────────────────────────────────────┐
│                         LAMBDA FUNCTIONS                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │ API Handler  │  │   Telegram   │  │  Publisher           │ │
│  │ - Get briefs │  │   Webhook    │  │  - Format messages   │ │
│  │ - Prefs CRUD │  │   - /start   │  │  - Send to users     │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                                │
                                │ Triggered by
                                ▼
┌────────────────────────────────────────────────────────────────┐
│                    STEP FUNCTIONS WORKFLOW                      │
│                    (Every 6 hours via EventBridge)              │
│                                                                 │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐            │
│  │  Fetch   │  →   │  Editor  │  →   │ Publish  │            │
│  │  News    │      │  (AI)    │      │  Brief   │            │
│  └──────────┘      └──────────┘      └──────────┘            │
└────────────────────────────────────────────────────────────────┘
       │                    │                    │
       │ Store              │ AI Analysis        │ Read/Write
       ▼                    ▼                    ▼
┌──────────────┐   ┌──────────────────┐   ┌──────────────┐
│  DynamoDB    │   │ Amazon Bedrock   │   │  DynamoDB    │
│  news_table  │   │ Claude 3.5       │   │ briefs_table │
│  (24h TTL)   │   │ - Select stories │   │ users_table  │
└──────────────┘   │ - Write summaries│   └──────────────┘
                   └──────────────────┘
                            │
                            │ Fetch from
                            ▼
                   ┌──────────────────┐
                   │  External APIs   │
                   │  - CryptoCompare │
                   │  - CoinDesk RSS  │
                   └──────────────────┘
```

## Data Flow

### 1. News Curation Workflow (Every 6 hours)

```
EventBridge Scheduler
    ↓
Step Functions Start
    ↓
┌─────────────────────────────────────────────────────────┐
│ STEP 1: Fetch News                                      │
│ Lambda: fetcher.py                                      │
│ - Call CryptoCompare API                                │
│ - Parse and normalize data                              │
│ - Store in DynamoDB (news_table) with 24h TTL           │
│ - Return: {statusCode: 200, count: 20}                  │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│ STEP 2: AI Editor Analysis                              │
│ Lambda: editor.py                                       │
│ - Query DynamoDB for stories from last 6 hours          │
│ - Format stories for AI prompt                          │
│ - Call Bedrock Claude:                                  │
│   • Prompt 1: Select top 3-5 stories (importance)       │
│   • Prompt 2: Write summaries for each (60-80 words)    │
│ - Store brief in DynamoDB (briefs_table)                │
│ - Return: {briefId, stories[], publishedAt}             │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│ STEP 3: Publish to Users                                │
│ Lambda: publisher.py                                    │
│ - Query all users from DynamoDB (users_table)           │
│ - Format brief as HTML message                          │
│ - Send via Telegram Bot API to each user                │
│ - Return: {sentTo: 150, totalUsers: 150}                │
└─────────────────────────────────────────────────────────┘
```

### 2. User Interaction Flow

```
User opens Telegram Mini App
    ↓
Telegram WebApp SDK initializes
    ↓
React Router v7 app loads from CloudFront
    ↓
GET /briefs (API Gateway → Lambda)
    ↓
Query DynamoDB briefs_table (last 10 briefs)
    ↓
Display in UI with:
    - Story titles
    - AI-generated summaries
    - Source attribution
    - Read more links
    ↓
User clicks "Settings"
    ↓
GET /preferences (API Gateway → Lambda)
    ↓
Query DynamoDB users_table
    ↓
Display preferences (topics, frequency)
    ↓
User updates preferences
    ↓
POST /preferences (API Gateway → Lambda)
    ↓
Update DynamoDB users_table
```

### 3. User Registration Flow

```
User sends /start to Telegram bot
    ↓
Telegram sends webhook to API Gateway
    ↓
Lambda: telegram_webhook.py
    ↓
Extract user info (userId, username, firstName)
    ↓
Store in DynamoDB users_table with default preferences:
    {
        userId: "123456789",
        username: "cryptofan",
        preferences: {
            topics: ["all"],
            frequency: "every_6_hours"
        },
        createdAt: 1234567890
    }
    ↓
Send welcome message via Telegram Bot API
```

## AI Agent Architecture

### Agent Identity: Editor-in-Chief

**Model**: Claude 3.5 Sonnet (anthropic.claude-3-5-sonnet-20241022-v2:0)

**Responsibilities**:
1. Story Selection (Importance Scoring)
2. Summary Generation (Concise Writing)
3. Editorial Judgment (Quality Control)

### Agent Tools

```python
# Tool 1: News Analyzer
def analyze_stories(stories: List[Story]) -> List[Selection]:
    """
    Input: 20-30 raw news stories
    Process: 
        - Evaluate market impact
        - Check source credibility
        - Detect duplicates
        - Score importance (1-10)
    Output: Top 3-5 story IDs with reasoning
    """

# Tool 2: Summary Writer
def write_summary(story: Story) -> str:
    """
    Input: Full news article
    Process:
        - Extract key facts
        - Remove speculation
        - Write 60-80 word summary
        - Maintain professional tone
    Output: Concise summary text
    """

# Tool 3: Deduplicator
def deduplicate(stories: List[Story]) -> List[Story]:
    """
    Input: Multiple stories
    Process:
        - Compare titles and content
        - Identify same event from different sources
        - Keep highest quality version
    Output: Unique stories only
    """
```

### Agent Memory

**Short-term Memory** (DynamoDB news_table, 24h TTL):
- Current news cycle stories
- Importance scores
- Processing status

**Long-term Memory** (DynamoDB):
- User engagement patterns (users_table)
- Historical briefs (briefs_table)
- Source credibility scores (future enhancement)

**Episodic Memory**:
- Last 10 published briefs
- User click-through rates per story
- Topic preferences per user

## AWS Services Breakdown

### Compute
- **Lambda Functions**: 6 functions
  - fetcher.py (news collection)
  - editor.py (AI curation)
  - publisher.py (Telegram delivery)
  - telegram_webhook.py (bot commands)
  - api.py (Mini App API)
- **Step Functions**: Orchestrate workflow
- **EventBridge**: Schedule triggers (every 6 hours)

### Storage
- **DynamoDB**: 3 tables
  - users (user profiles, preferences)
  - news (temporary cache, 24h TTL)
  - briefs (published content, 30 days)
- **S3**: Frontend static assets

### AI/ML
- **Amazon Bedrock**: Claude 3.5 Sonnet
  - Story selection (200-500 tokens per request)
  - Summary generation (100-200 tokens per story)
  - ~2000 tokens per brief cycle

### Networking
- **API Gateway**: REST API for Mini App
- **CloudFront**: CDN for frontend
- **Secrets Manager**: Bot token storage

### Monitoring
- **CloudWatch Logs**: All Lambda logs
- **CloudWatch Metrics**: Invocation counts, errors
- **X-Ray**: Distributed tracing (optional)

## Cost Breakdown (1000 users, 4 briefs/day)

```
Monthly Costs:
├─ Lambda
│  ├─ Invocations: 120K/month (4 briefs × 30 days × 1000 users)
│  ├─ Duration: ~500ms average
│  └─ Cost: ~$5
├─ DynamoDB
│  ├─ Storage: ~10GB (briefs + users)
│  ├─ Reads: 120K/month
│  ├─ Writes: 5K/month
│  └─ Cost: ~$10
├─ Bedrock (Claude 3.5 Sonnet)
│  ├─ Input tokens: ~300K/month (prompts)
│  ├─ Output tokens: ~200K/month (responses)
│  ├─ Rate: $3/$15 per 1M tokens
│  └─ Cost: ~$30
├─ S3 + CloudFront
│  ├─ Storage: <1GB
│  ├─ Requests: 30K/month
│  └─ Cost: ~$5
└─ Total: ~$50/month
```

## Scalability

### Current Capacity
- **Users**: 1,000 (no changes needed)
- **Briefs**: 4 per day (configurable)
- **Stories per brief**: 3-5 (AI-selected)

### Scale to 10,000 users
- Lambda: Auto-scales (no changes)
- DynamoDB: On-demand mode handles it
- Bedrock: Same token usage (per brief, not per user)
- Cost: ~$80/month (+$30 for DynamoDB)

### Scale to 100,000 users
- Lambda: Add reserved concurrency
- DynamoDB: Consider provisioned capacity
- Bedrock: Same token usage
- Add: SQS for message queuing
- Cost: ~$200/month

## Security

- **API Gateway**: CORS enabled, rate limiting
- **Lambda**: IAM roles with least privilege
- **DynamoDB**: Encryption at rest
- **Secrets Manager**: Bot token encrypted
- **Telegram**: Validate initData signature (production)
- **CloudFront**: HTTPS only

## Monitoring & Alerts

```
CloudWatch Alarms:
├─ Lambda Errors > 5% → SNS notification
├─ DynamoDB Throttling > 0 → Auto-scale
├─ Step Functions Failed → SNS notification
└─ Bedrock Latency > 10s → Investigation
```

## Future Enhancements

1. **Multi-language support**: Bedrock translation
2. **Sentiment analysis**: Track market mood
3. **Breaking news alerts**: Real-time push notifications
4. **User engagement ML**: Personalized curation
5. **Admin dashboard**: Analytics and controls
6. **A/B testing**: Optimize AI prompts
