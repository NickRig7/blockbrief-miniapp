#!/usr/bin/env python3
"""
BlockBrief Bot - Sends Mini App via Telegram Web App
"""
import json
import urllib.request
import time

BOT_TOKEN = "8208598337:AAFZ1E08dKgW86hd69BshsYEsc-5bXiIlqA"
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text, reply_markup=None):
    url = f"{TELEGRAM_API}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    if reply_markup:
        data['reply_markup'] = reply_markup
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

def fetch_real_news():
    """Fetch real crypto news"""
    try:
        url = 'https://min-api.cryptocompare.com/data/v2/news/?lang=EN'
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            stories = []
            for item in data.get('Data', [])[:5]:
                stories.append({
                    'title': item['title'],
                    'body': item['body'][:200] + '...',
                    'url': item['url'],
                    'source': item['source_info']['name'],
                    'imageUrl': item.get('imageurl', '')
                })
            return stories
    except:
        return []

def format_news_message(stories):
    """Format news as Telegram message"""
    message = "📰 <b>BlockBrief - Latest Crypto News</b>\n\n"
    
    for i, story in enumerate(stories, 1):
        message += f"<b>{i}. {story['title']}</b>\n"
        message += f"{story['body']}\n"
        message += f"🔗 <a href='{story['url']}'>Read more</a> • {story['source']}\n\n"
    
    message += "━━━━━━━━━━━━━━━━\n"
    message += "💎 Powered by AI"
    return message

def get_updates():
    offset = 0
    
    print("\n" + "="*80)
    print("  📰 BLOCKBRIEF BOT - RUNNING")
    print("="*80)
    print("\n✅ Bot is ready!")
    print("📱 Open Telegram → @block_briefbot → Send /news\n")
    print("="*80 + "\n")
    
    while True:
        try:
            url = f"{TELEGRAM_API}/getUpdates?offset={offset}&timeout=30"
            
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if data['ok'] and data['result']:
                    for update in data['result']:
                        offset = update['update_id'] + 1
                        
                        if 'message' in update:
                            message = update['message']
                            chat_id = message['chat']['id']
                            text = message.get('text', '')
                            
                            print(f"📨 Message: {text}")
                            
                            if text == '/start':
                                welcome = """<b>Welcome to BlockBrief! 🚀</b>

Your AI-powered crypto news curator.

<b>Commands:</b>
/news - Get latest crypto news
/start - Show this message

Tap /news to see today's top stories!"""
                                send_message(chat_id, welcome)
                                print("   → Sent welcome\n")
                            
                            elif text == '/news':
                                print("   → Fetching real news...")
                                stories = fetch_real_news()
                                if stories:
                                    msg = format_news_message(stories)
                                    send_message(chat_id, msg)
                                    print("   → Sent news\n")
                                else:
                                    send_message(chat_id, "Failed to fetch news. Try again!")
        
        except KeyboardInterrupt:
            print("\n\n👋 Bot stopped")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    get_updates()
