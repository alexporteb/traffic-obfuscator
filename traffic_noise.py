#!/usr/bin/env python3
"""
Traffic Noise Generator
Скрипт для фоновой генерации входящего HTTP/HTTPS трафика, 
чтобы скрыть симметрию In/Out на прокси-серверах.
"""

import time
import random
import logging
import urllib.request
import urllib.error

# === КОНФИГУРАЦИЯ ===

# Целевой объем трафика в сутки (в гигабайтах)
TARGET_GB_PER_DAY = 50.0

# Интервалы между скачиваниями (в секундах)
SLEEP_MIN_SECONDS = 300   # 5 минут
SLEEP_MAX_SECONDS = 1500  # 25 минут

# Файлы для скачивания (ISO-образы и тестовые дампы)
URLS = [
    "http://speedtest.tele2.net/1GB.zip",
    "http://speedtest.tele2.net/10GB.zip",
    "http://speedtest.tele2.net/100GB.zip",
    "https://speed.hetzner.de/100MB.bin",
    "https://speed.hetzner.de/1GB.bin",
    "https://speed.hetzner.de/10GB.bin",
    "http://ipv4.download.thinkbroadband.com/1GB.zip",
    "http://ipv4.download.thinkbroadband.com/512MB.zip",
    "https://releases.ubuntu.com/22.04/ubuntu-22.04.4-desktop-amd64.iso",
    "https://cdimage.debian.org/debian-cd/current/amd64/iso-dvd/debian-12.5.0-amd64-DVD-1.iso",
    "https://mirror.yandex.ru/ubuntu-releases/24.04/ubuntu-24.04-desktop-amd64.iso",
    "https://download.freebsd.org/releases/amd64/amd64/ISO-IMAGES/14.0/FreeBSD-14.0-RELEASE-amd64-dvd1.iso",
    "http://mirror.yandex.ru/centos/8-stream/isos/x86_64/CentOS-Stream-8-x86_64-latest-dvd1.iso"
]

# Актуальные User-Agent современных браузеров
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
]

# Настройка логирования (пишем в stdout для journalctl)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

def get_target_bytes_for_session() -> int:
    """Вычисляет целевой размер скачивания для одной сессии, чтобы достичь дневной нормы."""
    target_bytes_per_day = TARGET_GB_PER_DAY * 1024 * 1024 * 1024
    
    # Среднее время сна между загрузками
    avg_sleep_seconds = (SLEEP_MIN_SECONDS + SLEEP_MAX_SECONDS) / 2
    
    # Количество ожидаемых сессий в сутки
    sessions_per_day = (24 * 3600) / avg_sleep_seconds
    
    # Средний размер одной сессии для выполнения плана
    avg_bytes_per_session = target_bytes_per_day / sessions_per_day
    
    # Добавляем случайный разброс от -50% до +50% для размытия паттерна
    min_bytes = max(10 * 1024 * 1024, int(avg_bytes_per_session * 0.5))  # Не менее 10 МБ
    max_bytes = int(avg_bytes_per_session * 1.5)
    
    return random.randint(min_bytes, max_bytes)

def download_chunk(url: str, max_bytes: int) -> int:
    """Скачивает данные из потока и сразу же их отбрасывает."""
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    req = urllib.request.Request(url, headers=headers)
    downloaded_bytes = 0
    
    logging.info(f"Подключение к: {url}")
    logging.info(f"Целевой объем скачивания: {max_bytes / (1024*1024):.2f} MB")
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            while downloaded_bytes < max_bytes:
                # Читаем чанками по 64 KB и ничего с ними не делаем
                chunk = response.read(65536)
                if not chunk:
                    logging.info("Поток завершен сервером (файл оказался меньше цели).")
                    break
                downloaded_bytes += len(chunk)
                
            if downloaded_bytes >= max_bytes:
                logging.info("Целевой объем достигнут, принудительно разрываем соединение.")
                
    except urllib.error.URLError as e:
        logging.error(f"Сетевая ошибка при скачивании: {e}")
    except Exception as e:
        logging.error(f"Непредвиденная ошибка: {e}")
    
    logging.info(f"Сессия завершена. Фактически скачано: {downloaded_bytes / (1024*1024):.2f} MB")
    return downloaded_bytes

def main():
    logging.info("=== Запуск генератора фонового шума ===")
    logging.info(f"Целевой объем трафика в сутки: {TARGET_GB_PER_DAY} GB")
    
    while True:
        target_bytes = get_target_bytes_for_session()
        url = random.choice(URLS)
        
        download_chunk(url, target_bytes)
        
        sleep_seconds = random.randint(SLEEP_MIN_SECONDS, SLEEP_MAX_SECONDS)
        logging.info(f"Ожидание {sleep_seconds // 60} мин {sleep_seconds % 60} сек до следующей сессии...\n")
        time.sleep(sleep_seconds)

if __name__ == "__main__":
    # Пауза при старте, чтобы сеть успела подняться (полезно при автозапуске)
    time.sleep(10)
    main()
