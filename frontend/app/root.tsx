import { Links, Meta, Outlet, Scripts, ScrollRestoration } from "react-router";

export default function Root() {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />
        <Meta />
        <Links />
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <style>{`
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
          }
          
          .container {
            max-width: 100%;
            padding: 16px;
            padding-bottom: 80px;
          }
          
          .header {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 20px 0;
            border-bottom: 1px solid var(--tg-theme-hint-color, #e0e0e0);
            margin-bottom: 20px;
          }
          
          .logo {
            font-size: 32px;
          }
          
          .header-text h1 {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 4px;
          }
          
          .header-text p {
            font-size: 14px;
            color: var(--tg-theme-hint-color, #999);
          }
          
          .brief-card {
            background: var(--tg-theme-secondary-bg-color, #f5f5f5);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
          }
          
          .brief-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
          }
          
          .brief-time {
            font-size: 13px;
            color: var(--tg-theme-hint-color, #999);
          }
          
          .story {
            margin-bottom: 24px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--tg-theme-hint-color, #e0e0e0);
          }
          
          .story:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
          }
          
          .story-number {
            display: inline-block;
            background: var(--tg-theme-button-color, #3390ec);
            color: var(--tg-theme-button-text-color, #ffffff);
            width: 24px;
            height: 24px;
            border-radius: 50%;
            text-align: center;
            line-height: 24px;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 8px;
          }
          
          .story-title {
            font-size: 17px;
            font-weight: 600;
            margin-bottom: 8px;
            line-height: 1.4;
          }
          
          .story-summary {
            font-size: 15px;
            line-height: 1.5;
            margin-bottom: 12px;
            color: var(--tg-theme-text-color, #000);
          }
          
          .story-meta {
            display: flex;
            gap: 12px;
            align-items: center;
            font-size: 13px;
            color: var(--tg-theme-hint-color, #999);
          }
          
          .story-link {
            color: var(--tg-theme-link-color, #3390ec);
            text-decoration: none;
            font-weight: 500;
          }
          
          .loading {
            text-align: center;
            padding: 40px;
            color: var(--tg-theme-hint-color, #999);
          }
          
          .empty {
            text-align: center;
            padding: 60px 20px;
          }
          
          .empty-icon {
            font-size: 64px;
            margin-bottom: 16px;
          }
          
          .empty-text {
            font-size: 16px;
            color: var(--tg-theme-hint-color, #999);
          }
          
          .nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: var(--tg-theme-bg-color, #ffffff);
            border-top: 1px solid var(--tg-theme-hint-color, #e0e0e0);
            display: flex;
            padding: 8px 0;
          }
          
          .nav-item {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            padding: 8px;
            text-decoration: none;
            color: var(--tg-theme-hint-color, #999);
            font-size: 11px;
            transition: color 0.2s;
          }
          
          .nav-item.active {
            color: var(--tg-theme-button-color, #3390ec);
          }
          
          .nav-icon {
            font-size: 24px;
          }
          
          .preferences-section {
            margin-bottom: 24px;
          }
          
          .section-title {
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 12px;
            color: var(--tg-theme-hint-color, #999);
            text-transform: uppercase;
            letter-spacing: 0.5px;
          }
          
          .option {
            background: var(--tg-theme-secondary-bg-color, #f5f5f5);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
          }
          
          .option-label {
            font-size: 16px;
          }
          
          .toggle {
            width: 51px;
            height: 31px;
            background: var(--tg-theme-hint-color, #ccc);
            border-radius: 31px;
            position: relative;
            cursor: pointer;
            transition: background 0.3s;
          }
          
          .toggle.active {
            background: var(--tg-theme-button-color, #3390ec);
          }
          
          .toggle-thumb {
            width: 27px;
            height: 27px;
            background: white;
            border-radius: 50%;
            position: absolute;
            top: 2px;
            left: 2px;
            transition: left 0.3s;
          }
          
          .toggle.active .toggle-thumb {
            left: 22px;
          }
          
          .save-button {
            background: var(--tg-theme-button-color, #3390ec);
            color: var(--tg-theme-button-text-color, #ffffff);
            border: none;
            border-radius: 12px;
            padding: 16px;
            width: 100%;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 20px;
          }
        `}</style>
      </head>
      <body>
        <Outlet />
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  );
}
