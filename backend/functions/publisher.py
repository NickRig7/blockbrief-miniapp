import os
import json
import boto3
import requests

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table(os.environ['USERS_TABLE'])

TELEGRAM_API = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}"

def send_telegram_message(chat_id, text, parse_mode='HTML'):
    """Send message via Telegram Bot API"""
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': parse_mode,
        'disable_web_page_preview': False
    }
    response = requests.post(url, json=payload)
    return response.json()

def format_brief(stories, published_at):
    """Format brief for Telegram"""
    from datetime import datetime
    
    time_str = datetime.fromtimestamp(published_at).strftime('%B %d, %Y at %H:%M UTC')
    
    message = f"📰 <b>BlockBrief</b> • {time_str}\n\n"
    
    for i, story in enumerate(stories, 1):
        message += f"<b>{i}. {story['title']}</b>\n"
        message += f"{story['summary']}\n"
        message += f"🔗 <a href='{story['url']}'>Read more</a> • {story['source']}\n\n"
    
    message += "━━━━━━━━━━━━━━━━\n"
    message += "💎 Powered by AI • Open Mini App for preferences"
    
    return message

def handler(event, context):
    """Publish brief to all subscribed users"""
    
    brief_id = event.get('briefId')
    stories = event.get('stories', [])
    published_at = event.get('publishedAt')
    
    if not stories:
        return {'statusCode': 200, 'message': 'No stories to publish'}
    
    # Get all users
    response = users_table.scan()
    users = response.get('Items', [])
    
    # Format message
    message = format_brief(stories, published_at)
    
    # Send to all users
    sent_count = 0
    for user in users:
        try:
            send_telegram_message(user['userId'], message)
            sent_count += 1
        except Exception as e:
            print(f"Error sending to {user['userId']}: {e}")
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'briefId': brief_id,
            'sentTo': sent_count,
            'totalUsers': len(users)
        })
    }
