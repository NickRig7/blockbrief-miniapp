# 🚀 Deploy BlockBrief Mini App (2 Minutes)

## The Problem
Localtunnel requires a password page. To bypass this, we need to host the Mini App on a public service.

## ✅ Quickest Solution (Choose One):

### Option 1: GitHub Gist (Easiest - 2 minutes)

1. Go to: https://gist.github.com
2. Create new gist (no login needed for public gist)
3. Filename: `miniapp.html`
4. Paste the content from: `/workshop/blockbrief/miniapp.html`
5. Click "Create public gist"
6. Click the "Raw" button
7. Copy the URL (looks like: `https://gist.githubusercontent.com/...`)
8. Run this command with your URL:

```bash
curl -X POST "https://api.telegram.org/bot8208598337:AAFZ1E08dKgW86hd69BshsYEsc-5bXiIlqA/setChatMenuButton" \
  -H "Content-Type: application/json" \
  -d '{"menu_button":{"type":"web_app","text":"Open BlockBrief","web_app":{"url":"YOUR_GIST_RAW_URL"}}}'
```

### Option 2: Netlify Drop (No signup - 1 minute)

1. Go to: https://app.netlify.com/drop
2. Drag `/workshop/blockbrief/miniapp.html` onto the page
3. Get instant URL (like: `https://something.netlify.app`)
4. Run the command above with your Netlify URL

### Option 3: Vercel (Requires signup - 3 minutes)

1. Go to: https://vercel.com
2. Sign up (free)
3. Create new project
4. Upload `miniapp.html`
5. Deploy
6. Get URL
7. Run the command above

## 🎬 After Deployment

1. Open Telegram
2. Go to @block_briefbot
3. Tap "Open BlockBrief" button
4. Mini App opens with real crypto news!

## 📱 What You'll See

- Beautiful card-based layout
- Real crypto news with images
- Smooth scrolling
- Refresh button
- Professional UI

## 💡 For Demo

This is perfect for your hackathon because:
- ✅ Real data from CryptoCompare API
- ✅ Beautiful, production-ready UI
- ✅ Works in actual Telegram
- ✅ No password prompts
- ✅ Professional presentation

---

**Choose Option 1 (GitHub Gist) - it's the fastest!**
