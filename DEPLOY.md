# 🚀 Deploy BlockBrief to GitHub Pages

## Quick Steps (2 minutes)

### 1. Push to GitHub

```bash
cd /workshop/blockbrief-miniapp

# Add your GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/blockbrief-miniapp.git

# Push
git push -u origin main
```

### 2. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings**
3. Click **Pages** (left sidebar)
4. Under "Source", select **main** branch
5. Click **Save**
6. Wait 1 minute - your site will be live at:
   `https://YOUR_USERNAME.github.io/blockbrief-miniapp`

### 3. Set Telegram Bot URL

```bash
curl -X POST "https://api.telegram.org/bot8208598337:AAFZ1E08dKgW86hd69BshsYEsc-5bXiIlqA/setChatMenuButton" \
  -H "Content-Type: application/json" \
  -d '{"menu_button":{"type":"web_app","text":"Open BlockBrief","web_app":{"url":"https://YOUR_USERNAME.github.io/blockbrief-miniapp"}}}'
```

### 4. Test

1. Open Telegram
2. Go to @block_briefbot
3. Tap "Open BlockBrief"
4. See your Mini App with real crypto news!

## What You Have

✅ Complete Telegram Mini App
✅ Real crypto news from CryptoCompare
✅ Beautiful, responsive UI
✅ Telegram WebApp SDK integrated
✅ Auto-refresh every 5 minutes
✅ Ready for GitHub Pages

## Files

- `index.html` - Complete Mini App (single file!)
- `README.md` - Documentation
- `.git/` - Git repository

## Next Steps

1. Create GitHub repository: https://github.com/new
2. Name it: `blockbrief-miniapp`
3. Make it Public
4. Follow the push commands above
5. Enable GitHub Pages
6. Update bot URL
7. Done!

---

**Your Mini App is ready to deploy!** 🎉
