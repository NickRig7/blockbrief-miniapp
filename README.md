# BlockBrief - Telegram Mini App

AI-powered crypto news curator delivered via Telegram Mini App.

## Features

- 📰 Real-time crypto news from CryptoCompare API
- 🎨 Beautiful, responsive UI with Telegram theming
- 🔄 Auto-refresh every 5 minutes
- 📱 Native Telegram Mini App experience
- ⚡ Fast loading and smooth animations

## Demo

Visit the live app: [Your GitHub Pages URL]

## Setup

1. Clone this repository
2. Enable GitHub Pages in repository settings
3. Set the GitHub Pages URL in your Telegram bot via @BotFather

## Telegram Bot Setup

1. Create a bot with @BotFather
2. Get your bot token
3. Set the Mini App URL:
   ```
   /setmenubutton
   Select your bot
   Send your GitHub Pages URL
   ```

## Local Development

Simply open `index.html` in a browser to test locally.

## Deployment

### GitHub Pages (Recommended)
1. Push to GitHub
2. Go to Settings → Pages
3. Enable GitHub Pages from main branch
4. Your app will be live at: `https://YOUR_USERNAME.github.io/REPO_NAME`

### Other Options
- Netlify: Drag and drop `index.html`
- Vercel: Import repository
- Any static hosting service

## Architecture

- **Frontend**: Vanilla JavaScript (no frameworks)
- **API**: CryptoCompare free tier
- **Telegram**: WebApp SDK
- **Styling**: CSS with Telegram theme variables

## Future Enhancements

- AI curation with AWS Lambda + Bedrock
- User preferences
- Push notifications
- Brief history
- Multi-language support

## License

MIT
