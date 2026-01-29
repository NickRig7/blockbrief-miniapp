import os
import json
import time
import boto3
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

news_table = dynamodb.Table(os.environ['NEWS_TABLE'])
briefs_table = dynamodb.Table(os.environ['BRIEFS_TABLE'])

EDITOR_PROMPT = """You are the AI Editor-in-Chief of BlockBrief, a premium crypto news service.

Your job: Analyze these crypto news stories and select the TOP 3-5 most important ones for today's brief.

SELECTION CRITERIA (in order of importance):
1. Market Impact - Major price movements, exchange news, institutional adoption
2. Regulatory Significance - Government actions, legal developments
3. Technical Innovation - Protocol upgrades, new tech launches
4. Credibility - Prefer established sources over rumors
5. Timeliness - Recent stories over old news

AVOID:
- Duplicate stories (same event from different sources)
- Minor altcoin pumps
- Clickbait without substance
- Opinion pieces without news value

STORIES:
{stories}

OUTPUT FORMAT (JSON only):
{{
  "selected": [
    {{
      "storyId": "123",
      "reasoning": "Major exchange hack affecting $100M+ in user funds",
      "importance": 9
    }}
  ]
}}

Select 3-5 stories. Return ONLY valid JSON."""

WRITER_PROMPT = """You are writing a crypto news brief for BlockBrief. 

Write a concise, engaging summary (60-80 words) for this story:

TITLE: {title}
CONTENT: {body}
SOURCE: {source}

STYLE:
- Clear, direct language
- Lead with the most important fact
- No hype or speculation
- Professional but accessible

OUTPUT: Just the summary text, no JSON."""

def get_recent_stories():
    """Get stories from last 6 hours"""
    cutoff = int(time.time()) - 21600  # 6 hours
    
    response = news_table.scan(
        FilterExpression='#ts > :cutoff',
        ExpressionAttributeNames={'#ts': 'timestamp'},
        ExpressionAttributeValues={':cutoff': cutoff}
    )
    return response.get('Items', [])

def call_bedrock(prompt, max_tokens=2000):
    """Call Claude via Bedrock"""
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    })
    
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
        body=body
    )
    
    result = json.loads(response['body'].read())
    return result['content'][0]['text']

def handler(event, context):
    """AI Editor: Analyze, select, and write brief"""
    
    # Get recent stories
    stories = get_recent_stories()
    
    if len(stories) < 3:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Not enough stories to curate'})
        }
    
    # Format stories for AI
    stories_text = "\n\n".join([
        f"ID: {s['storyId']}\nTitle: {s['title']}\nSource: {s['source']}\nBody: {s['body'][:300]}"
        for s in stories[:30]  # Limit to 30 most recent
    ])
    
    # Step 1: AI selects top stories
    selection_response = call_bedrock(EDITOR_PROMPT.format(stories=stories_text))
    
    # Parse selection
    try:
        # Extract JSON from response
        json_start = selection_response.find('{')
        json_end = selection_response.rfind('}') + 1
        selection_data = json.loads(selection_response[json_start:json_end])
        selected_ids = [s['storyId'] for s in selection_data['selected']]
    except:
        # Fallback: take first 3 stories
        selected_ids = [s['storyId'] for s in stories[:3]]
    
    # Step 2: AI writes summaries
    brief_stories = []
    for story_id in selected_ids[:5]:
        story = next((s for s in stories if s['storyId'] == story_id), None)
        if not story:
            continue
        
        summary = call_bedrock(
            WRITER_PROMPT.format(
                title=story['title'],
                body=story['body'],
                source=story['source']
            ),
            max_tokens=200
        )
        
        brief_stories.append({
            'storyId': story['storyId'],
            'title': story['title'],
            'summary': summary.strip(),
            'url': story['url'],
            'source': story['source'],
            'imageUrl': story.get('imageUrl', '')
        })
    
    # Save brief
    brief_id = f"brief-{int(time.time())}"
    published_at = int(time.time())
    
    briefs_table.put_item(
        Item={
            'briefId': brief_id,
            'stories': brief_stories,
            'publishedAt': published_at,
            'storyCount': len(brief_stories)
        }
    )
    
    return {
        'statusCode': 200,
        'briefId': brief_id,
        'stories': brief_stories,
        'publishedAt': published_at
    }
