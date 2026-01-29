import os
import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table(os.environ['USERS_TABLE'])
briefs_table = dynamodb.Table(os.environ['BRIEFS_TABLE'])

def cors_response(status_code, body):
    """Return CORS-enabled response"""
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Telegram-Init-Data',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }

def get_user_id_from_telegram_data(init_data):
    """Extract user ID from Telegram init data (simplified)"""
    # In production, validate the init data signature
    # For MVP, extract user ID from query string
    try:
        import urllib.parse
        params = urllib.parse.parse_qs(init_data)
        user_data = json.loads(params.get('user', ['{}'])[0])
        return str(user_data.get('id'))
    except:
        return None

def handler(event, context):
    """API for Telegram Mini App"""
    
    path = event.get('path', '')
    method = event.get('httpMethod', '')
    
    # Get user ID from Telegram init data
    init_data = event.get('headers', {}).get('X-Telegram-Init-Data', '')
    user_id = get_user_id_from_telegram_data(init_data) if init_data else 'demo-user'
    
    # GET /briefs - Get recent briefs
    if path == '/briefs' and method == 'GET':
        response = briefs_table.scan(Limit=10)
        briefs = sorted(
            response.get('Items', []),
            key=lambda x: x.get('publishedAt', 0),
            reverse=True
        )
        return cors_response(200, {'briefs': briefs})
    
    # GET /preferences - Get user preferences
    elif path == '/preferences' and method == 'GET':
        try:
            response = users_table.get_item(Key={'userId': user_id})
            user = response.get('Item', {})
            preferences = user.get('preferences', {
                'topics': ['all'],
                'frequency': 'every_6_hours'
            })
            return cors_response(200, {'preferences': preferences})
        except:
            return cors_response(200, {
                'preferences': {
                    'topics': ['all'],
                    'frequency': 'every_6_hours'
                }
            })
    
    # POST /preferences - Update preferences
    elif path == '/preferences' and method == 'POST':
        try:
            body = json.loads(event.get('body', '{}'))
            preferences = body.get('preferences', {})
            
            users_table.update_item(
                Key={'userId': user_id},
                UpdateExpression='SET preferences = :prefs',
                ExpressionAttributeValues={':prefs': preferences}
            )
            
            return cors_response(200, {'success': True})
        except Exception as e:
            return cors_response(400, {'error': str(e)})
    
    return cors_response(404, {'error': 'Not found'})
