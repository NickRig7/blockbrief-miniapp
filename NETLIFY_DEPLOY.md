# 🚀 Final Solution - Deploy to Netlify (1 Minute)

## The Issue
GitHub Gist raw URLs serve as text/plain, not HTML, so they show code instead of rendering.

## ✅ Best Solution: Netlify Drop

1. **Go to:** https://app.netlify.com/drop
2. **Drag and drop** the file: `/workshop/blockbrief/miniapp.html`
3. **Wait 10 seconds** - you'll get a URL like: `https://something-random.netlify.app`
4. **Copy that URL**
5. **Run this command** with your URL:

```bash
curl -X POST "https://api.telegram.org/bot8208598337:AAFZ1E08dKgW86hd69BshsYEsc-5bXiIlqA/setChatMenuButton" \
  -H "Content-Type: application/json" \
  -d '{"menu_button":{"type":"web_app","text":"Open BlockBrief","web_app":{"url":"YOUR_NETLIFY_URL"}}}'
```

## Why Netlify?
- ✅ No signup required
- ✅ Instant deployment (10 seconds)
- ✅ Serves HTML properly
- ✅ Free forever
- ✅ HTTPS by default

## Alternative: Vercel

1. Go to: https://vercel.com
2. Sign up (free)
3. New project → Upload `miniapp.html`
4. Deploy
5. Use the URL

---

**Netlify Drop is the fastest - just drag and drop!**
