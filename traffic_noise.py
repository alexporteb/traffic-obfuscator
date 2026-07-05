#!/usr/bin/env python3
import time
import random
import logging
import urllib.request
import urllib.error

TARGET_GB_PER_DAY = 10.0
SLEEP_MIN_SECONDS = 300
SLEEP_MAX_SECONDS = 1500

URLS = [
    "https://mirror.yandex.ru/archlinux/iso/latest/archlinux-x86_64.iso",
    "https://mirror.yandex.ru/archlinux/iso/latest/archlinux-bootstrap-x86_64.tar.gz",
    "https://mirror.yandex.ru/centos/8-stream/isos/x86_64/CentOS-Stream-8-x86_64-latest-dvd1.iso",
    "https://mirror.yandex.ru/centos/9-stream/BaseOS/x86_64/iso/CentOS-Stream-9-latest-x86_64-dvd1.iso",
    "https://mirror.truenetwork.ru/archlinux/iso/latest/archlinux-x86_64.iso",
    "https://mirror.truenetwork.ru/archlinux/iso/latest/archlinux-bootstrap-x86_64.tar.gz",
    "https://mirror.truenetwork.ru/centos/8-stream/isos/x86_64/CentOS-Stream-8-x86_64-latest-dvd1.iso",
    "https://mirror.truenetwork.ru/centos/9-stream/BaseOS/x86_64/iso/CentOS-Stream-9-latest-x86_64-dvd1.iso",
    "http://speedtest.tele2.net/10GB.zip",
    "http://ipv4.download.thinkbroadband.com/1GB.zip",
    "http://proof.ovh.net/files/10Gb.dat",
    "http://mirror.leaseweb.com/speedtest/10000mb.bin"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
]

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

def get_target_bytes_for_session() -> int:
    target_bytes_per_day = TARGET_GB_PER_DAY * 1024 * 1024 * 1024
    avg_sleep_seconds = (SLEEP_MIN_SECONDS + SLEEP_MAX_SECONDS) / 2
    sessions_per_day = (24 * 3600) / avg_sleep_seconds
    avg_bytes_per_session = target_bytes_per_day / sessions_per_day
    min_bytes = max(10 * 1024 * 1024, int(avg_bytes_per_session * 0.5))
    max_bytes = int(avg_bytes_per_session * 1.5)
    return random.randint(min_bytes, max_bytes)

def download_chunk(url: str, max_bytes: int) -> int:
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    req = urllib.request.Request(url, headers=headers)
    downloaded_bytes = 0
    logging.info(f"Target: {url}")
    logging.info(f"Size: {max_bytes / (1024*1024):.2f} MB")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            while downloaded_bytes < max_bytes:
                chunk = response.read(65536)
                if not chunk:
                    break
                downloaded_bytes += len(chunk)
            if downloaded_bytes >= max_bytes:
                logging.info("Target volume reached.")
    except urllib.error.URLError as e:
        logging.error(f"Network error: {e}")
    except Exception as e:
        logging.error(f"Error: {e}")
    
    logging.info(f"Session finished. Downloaded: {downloaded_bytes / (1024*1024):.2f} MB")
    return downloaded_bytes

def main():
    logging.info("Starting sys-metrics...")
    while True:
        target_bytes = get_target_bytes_for_session()
        url = random.choice(URLS)
        download_chunk(url, target_bytes)
        sleep_seconds = random.randint(SLEEP_MIN_SECONDS, SLEEP_MAX_SECONDS)
        logging.info(f"Sleeping for {sleep_seconds}s...\n")
        time.sleep(sleep_seconds)

if __name__ == "__main__":
    time.sleep(10)
    main()
