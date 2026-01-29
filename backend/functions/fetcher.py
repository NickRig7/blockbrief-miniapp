import os
import json
import time
import boto3
import requests
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
news_table = dynamodb.Table(os.environ['NEWS_TABLE'])

# Free crypto news sources
NEWS_SOURCES = [
    {
        'name': 'CoinDesk',
        'url': 'https://www.coindesk.com/arc/outboundfeeds/rss/',
        'type': 'rss'
    },
    {
        'name': 'CryptoCompare',
        'url': 'https://min-api.cryptocompare.com/data/v2/news/?lang=EN',
        'type': 'api'
    }
]

def fetch_cryptocompare():
    """Fetch from CryptoCompare free API"""
    try:
        response = requests.get(NEWS_SOURCES[1]['url'], timeout=10)
        data = response.json()
        stories = []
        
        for item in data.get('Data', [])[:20]:
            stories.append({
                'storyId': item['id'],
                'title': item['title'],
                'body': item['body'][:500],
                'url': item['url'],
                'source': item['source_info']['name'],
                'publishedAt': item['published_on'],
                'imageUrl': item.get('imageurl', ''),
                'categories': item.get('categories', '').split('|')
            })
        return stories
    except Exception as e:
        print(f"Error fetching CryptoCompare: {e}")
        return []

def handler(event, context):
    """Fetch crypto news and store in DynamoDB"""
    
    stories = fetch_cryptocompare()
    
    # Store in DynamoDB with 24h TTL
    timestamp = int(time.time())
    ttl = timestamp + 86400  # 24 hours
    
    stored_count = 0
    for story in stories:
        try:
            news_table.put_item(
                Item={
                    'storyId': str(story['storyId']),
                    'title': story['title'],
                    'body': story['body'],
                    'url': story['url'],
                    'source': story['source'],
                    'publishedAt': story['publishedAt'],
                    'imageUrl': story.get('imageUrl', ''),
                    'categories': story.get('categories', []),
                    'timestamp': timestamp,
                    'ttl': ttl,
                    'score': 0
                }
            )
            stored_count += 1
        except Exception as e:
            print(f"Error storing story {story['storyId']}: {e}")
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Fetched and stored {stored_count} stories',
            'timestamp': timestamp
        })
    }
