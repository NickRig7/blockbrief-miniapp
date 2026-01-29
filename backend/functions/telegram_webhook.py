import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table(os.environ['USERS_TABLE'])

def handler(event, context):
    """Handle Telegram bot webhook"""
    
    try:
        body = json.loads(event.get('body', '{}'))
        message = body.get('message', {})
        
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '')
        
        if not chat_id:
            return {'statusCode': 200}
        
        # Handle /start command
        if text.startswith('/start'):
            # Register user
            users_table.put_item(
                Item={
                    'userId': str(chat_id),
                    'username': message.get('from', {}).get('username', ''),
                    'firstName': message.get('from', {}).get('first_name', ''),
                    'preferences': {
                        'topics': ['all'],
                        'frequency': 'every_6_hours'
                    },
                    'createdAt': int(message.get('date', 0))
                }
            )
            
            # Send welcome message
            welcome_text = """Welcome to BlockBrief! 🚀

I'm your AI Editor-in-Chief, curating the most important crypto news every 6 hours.

You'll receive:
• 3-5 top stories per brief
• AI-analyzed for importance
• Concise summaries
• Direct links to full articles

Tap the menu button below to open the Mini App and customize your preferences!"""
            
            # Send via Telegram API (simplified - in production use requests)
            print(f"Send welcome to {chat_id}: {welcome_text}")
        
        return {'statusCode': 200}
        
    except Exception as e:
        print(f"Webhook error: {e}")
        return {'statusCode': 200}
