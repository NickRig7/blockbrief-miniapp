# BlockBrief Mini App 📱

Telegram Mini App for BlockBrief - AI-powered crypto news curator.

## Features

- 📰 Real-time crypto news from CryptoCompare API
- 🎨 Telegram design system with smooth animations
- 🔖 Save articles for later reading
- 🔍 Search and filter by category (Bitcoin, Crypto, Insights, Stocks)
- 📱 Native Telegram Mini App experience
- ⚡ Fast loading with staggered animations
- 🌙 Automatic theme support (light/dark)

## Live Demo

https://nickrig7.github.io/blockbrief-miniapp/

## Tech Stack

- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **API**: CryptoCompare News API (free tier)
- **Design**: Telegram UIKit design system
- **Telegram**: WebApp SDK
- **Hosting**: GitHub Pages

## Local Development

```bash
# Open directly in browser
open index.html

# Or run a local server
python3 -m http.server 8000
# Visit http://localhost:8000
```

## Deployment

This app is deployed to GitHub Pages. Any push to main branch automatically deploys.

## Telegram Bot Setup

1. Create a bot with @BotFather
2. Set the menu button:
   ```
   /mybots → Select bot → Bot Settings → Menu Button
   Enter URL: https://nickrig7.github.io/blockbrief-miniapp/
   ```

## Design System

Based on Telegram's official UIKit with:
- Spring animations (cubic-bezier easing)
- iOS-style components
- Telegram color variables
- Smooth transitions and micro-interactions

## Backend Integration

This Mini App can be integrated with the BlockBrief backend:
- Repository: https://github.com/YOUR_USERNAME/blockbrief
- Features: AI curation, user preferences, personalized briefs

## License

MIT
