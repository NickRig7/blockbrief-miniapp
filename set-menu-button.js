const https = require('https');

const BOT_TOKEN = process.env.BOT_TOKEN || process.argv[2];
const MENU_URL = 'https://nickrig7.github.io/blockbrief-miniapp/';

if (!BOT_TOKEN) {
    console.error('Usage: BOT_TOKEN=your_token node set-menu-button.js');
    console.error('   or: node set-menu-button.js your_token');
    process.exit(1);
}

const data = JSON.stringify({
    menu_button: {
        type: 'web_app',
        text: 'Open BlockBrief',
        web_app: { url: MENU_URL }
    }
});

const options = {
    hostname: 'api.telegram.org',
    path: `/bot${BOT_TOKEN}/setChatMenuButton`,
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length
    }
};

const req = https.request(options, (res) => {
    let body = '';
    res.on('data', (chunk) => body += chunk);
    res.on('end', () => {
        console.log('Response:', JSON.parse(body));
    });
});

req.on('error', (e) => console.error('Error:', e));
req.write(data);
req.end();
