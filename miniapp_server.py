#!/usr/bin/env python3
"""
BlockBrief Mini App Server
Serves the Telegram Mini App with real news
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import urllib.request
import time
from datetime import datetime

class MiniAppHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_mini_app_html().encode())
        elif self.path == '/api/news':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            news = self.fetch_real_news()
            self.wfile.write(json.dumps(news).encode())
        else:
            super().do_GET()
    
    def fetch_real_news(self):
        """Fetch real crypto news from CryptoCompare"""
        try:
            url = 'https://min-api.cryptocompare.com/data/v2/news/?lang=EN'
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
                
                stories = []
                for item in data.get('Data', [])[:10]:
                    stories.append({
                        'id': item['id'],
                        'title': item['title'],
                        'body': item['body'][:300] + '...',
                        'url': item['url'],
                        'source': item['source_info']['name'],
                        'publishedAt': item['published_on'],
                        'imageUrl': item.get('imageurl', '')
                    })
                
                return {
                    'success': True,
                    'stories': stories,
                    'timestamp': int(time.time())
                }
        except Exception as e:
            print(f"Error fetching news: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_mini_app_html(self):
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>BlockBrief</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--tg-theme-bg-color, #ffffff);
            color: var(--tg-theme-text-color, #000000);
            overflow-x: hidden;
            padding-bottom: 20px;
        }
        
        .header {
            position: sticky;
            top: 0;
            background: var(--tg-theme-bg-color, #ffffff);
            padding: 16px;
            border-bottom: 1px solid var(--tg-theme-hint-color, #e0e0e0);
            z-index: 100;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .logo {
            font-size: 32px;
        }
        
        .header-text h1 {
            font-size: 22px;
            font-weight: 700;
        }
        
        .header-text p {
            font-size: 13px;
            color: var(--tg-theme-hint-color, #999);
        }
        
        .loading {
            text-align: center;
            padding: 60px 20px;
            color: var(--tg-theme-hint-color, #999);
        }
        
        .spinner {
            border: 3px solid var(--tg-theme-hint-color, #f3f3f3);
            border-top: 3px solid var(--tg-theme-button-color, #3390ec);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 16px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .container {
            padding: 16px;
        }
        
        .story-card {
            background: var(--tg-theme-secondary-bg-color, #f5f5f5);
            border-radius: 16px;
            padding: 16px;
            margin-bottom: 16px;
            transition: transform 0.2s;
        }
        
        .story-card:active {
            transform: scale(0.98);
        }
        
        .story-image {
            width: 100%;
            height: 180px;
            object-fit: cover;
            border-radius: 12px;
            margin-bottom: 12px;
            background: var(--tg-theme-hint-color, #e0e0e0);
        }
        
        .story-meta {
            display: flex;
            gap: 8px;
            align-items: center;
            margin-bottom: 8px;
            font-size: 12px;
            color: var(--tg-theme-hint-color, #999);
        }
        
        .story-source {
            font-weight: 600;
            color: var(--tg-theme-button-color, #3390ec);
        }
        
        .story-time {
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        .story-title {
            font-size: 18px;
            font-weight: 700;
            line-height: 1.4;
            margin-bottom: 8px;
            color: var(--tg-theme-text-color, #000);
        }
        
        .story-body {
            font-size: 15px;
            line-height: 1.5;
            color: var(--tg-theme-text-color, #333);
            margin-bottom: 12px;
        }
        
        .read-more {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            color: var(--tg-theme-button-color, #3390ec);
            font-weight: 600;
            font-size: 14px;
            text-decoration: none;
        }
        
        .badge {
            display: inline-block;
            background: var(--tg-theme-button-color, #3390ec);
            color: var(--tg-theme-button-text-color, #ffffff);
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .refresh-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: var(--tg-theme-button-color, #3390ec);
            color: var(--tg-theme-button-text-color, #ffffff);
            border: none;
            font-size: 24px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.2s;
        }
        
        .refresh-btn:active {
            transform: scale(0.9);
        }
        
        .error {
            text-align: center;
            padding: 40px 20px;
            color: #e74c3c;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">📰</div>
        <div class="header-text">
            <h1>BlockBrief</h1>
            <p>Real-time Crypto News</p>
        </div>
    </div>
    
    <div id="app">
        <div class="loading">
            <div class="spinner"></div>
            <p>Loading latest crypto news...</p>
        </div>
    </div>
    
    <button class="refresh-btn" onclick="loadNews()" title="Refresh">🔄</button>
    
    <script>
        // Initialize Telegram WebApp
        const tg = window.Telegram.WebApp;
        tg.ready();
        tg.expand();
        
        function formatTime(timestamp) {
            const now = Date.now() / 1000;
            const diff = now - timestamp;
            
            if (diff < 3600) {
                const mins = Math.floor(diff / 60);
                return mins + 'm ago';
            } else if (diff < 86400) {
                const hours = Math.floor(diff / 3600);
                return hours + 'h ago';
            } else {
                const days = Math.floor(diff / 86400);
                return days + 'd ago';
            }
        }
        
        function openLink(url) {
            if (tg.openLink) {
                tg.openLink(url);
            } else {
                window.open(url, '_blank');
            }
        }
        
        function renderStories(stories) {
            const app = document.getElementById('app');
            
            if (!stories || stories.length === 0) {
                app.innerHTML = '<div class="error">No news available. Try refreshing.</div>';
                return;
            }
            
            const html = '<div class="container">' + stories.map(story => `
                <div class="story-card">
                    ${story.imageUrl ? `<img src="${story.imageUrl}" class="story-image" alt="${story.title}" onerror="this.style.display='none'">` : ''}
                    <div class="story-meta">
                        <span class="story-source">${story.source}</span>
                        <span>•</span>
                        <span class="story-time">🕐 ${formatTime(story.publishedAt)}</span>
                    </div>
                    <div class="story-title">${story.title}</div>
                    <div class="story-body">${story.body}</div>
                    <a href="#" class="read-more" onclick="event.preventDefault(); openLink('${story.url}')">
                        Read full article →
                    </a>
                </div>
            `).join('') + '</div>';
            
            app.innerHTML = html;
        }
        
        async function loadNews() {
            const app = document.getElementById('app');
            app.innerHTML = '<div class="loading"><div class="spinner"></div><p>Loading latest crypto news...</p></div>';
            
            try {
                const response = await fetch('/api/news');
                const data = await response.json();
                
                if (data.success) {
                    renderStories(data.stories);
                } else {
                    app.innerHTML = '<div class="error">Failed to load news. Please try again.</div>';
                }
            } catch (error) {
                console.error('Error:', error);
                app.innerHTML = '<div class="error">Network error. Please check your connection.</div>';
            }
        }
        
        // Load news on startup
        loadNews();
        
        // Auto-refresh every 5 minutes
        setInterval(loadNews, 300000);
    </script>
</body>
</html>'''
    
    def log_message(self, format, *args):
        pass  # Suppress default logging

if __name__ == '__main__':
    PORT = 8080
    print("\n" + "="*80)
    print("  📰 BLOCKBRIEF MINI APP SERVER")
    print("="*80)
    print(f"\n✅ Server running on: http://localhost:{PORT}")
    print(f"🌐 Public URL needed for Telegram")
    print("\n📱 To use in Telegram:")
    print("  1. You need to expose this to the internet (use ngrok or similar)")
    print("  2. Set the URL in @BotFather with /setmenubutton")
    print("\n🔄 Features:")
    print("  • Real-time crypto news from CryptoCompare")
    print("  • Beautiful Telegram Mini App UI")
    print("  • Auto-refresh every 5 minutes")
    print("  • Telegram WebApp SDK integration")
    print("\nPress Ctrl+C to stop\n")
    print("="*80 + "\n")
    
    server = HTTPServer(('0.0.0.0', PORT), MiniAppHandler)
    server.serve_forever()
