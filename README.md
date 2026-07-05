# Proxy Noise Generator 🥷

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)

**Proxy Noise Generator** is a lightweight, zero-dependency Python script designed to run as a background systemd service on Linux VPS. It generates randomized background HTTP/HTTPS download traffic to disrupt symmetric In/Out traffic patterns often associated with proxy servers or VPNs.

🇷🇺 [Русская версия (Russian version)](#русская-версия)

---

## 🌟 Features
* **Zero Disk I/O:** Streams data directly to memory and immediately discards it. It will never wear out your VPS SSD or fill up your storage.
* **Zero Dependencies:** Uses only Python's built-in `urllib`. No need for `pip install` or virtual environments.
* **Randomized Patterns:** Randomizes download sizes, intervals between sessions, and target URLs to prevent pattern fingerprinting.
* **User-Agent Spoofing:** Rotates through a list of modern browser User-Agents.
* **Resource Friendly:** Runs securely under the unprivileged `nobody` user with systemd-enforced CPU and Memory limits.

## ⚙️ Configuration
Open `traffic_noise.py` to adjust limits:
* `TARGET_GB_PER_DAY` — Target volume of traffic per day (default: `50.0` GB).
* `SLEEP_MIN_SECONDS` / `SLEEP_MAX_SECONDS` — Minimum and maximum sleep intervals between download sessions.

## 🚀 Installation & Setup (Linux systemd)

1. **Download the script:**
   ```bash
   sudo mkdir -p /opt/traffic-noise
   sudo wget -O /opt/traffic-noise/traffic_noise.py https://raw.githubusercontent.com/alexporteb/traffic-obfuscator/main/traffic_noise.py
   sudo chmod +x /opt/traffic-noise/traffic_noise.py
   ```

2. **Create a systemd service:**
   ```bash
   sudo nano /etc/systemd/system/traffic-noise.service
   ```
   *Paste the following:*
   ```ini
   [Unit]
   Description=Background Traffic Noise Generator
   After=network-online.target
   Wants=network-online.target

   [Service]
   Type=simple
   User=nobody
   ExecStart=/usr/bin/python3 /opt/traffic-noise/traffic_noise.py
   Restart=always
   RestartSec=30
   MemoryLimit=150M
   CPUQuota=20%

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and start the service:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now traffic-noise
   ```

4. **Check the logs:**
   ```bash
   sudo journalctl -u traffic-noise -f
   ```

---

## 🇷🇺 Русская версия 

**Proxy Noise Generator** — это легковесный Python-скрипт без зависимостей, предназначенный для работы в фоне на Linux VPS. Он генерирует случайный входящий трафик для размытия симметричного паттерна (соотношения In/Out), характерного для прокси-серверов и VPN. 

### Главные особенности:
* **Не использует диск:** Скрипт скачивает данные в оперативную память и сразу же их отбрасывает. Он не изнашивает SSD и не занимает место.
* **Без зависимостей:** Использует только встроенную библиотеку `urllib`. Не нужно ставить внешние пакеты через `pip`.
* **Полный рандом:** Случайный выбор файла, случайный объем скачивания (обрыв соединения) и случайные паузы между сессиями (нет тайминг-паттерна).
* **Маскировка (User-Agent):** Автоматически подставляет актуальные заголовки современных браузеров Chrome, Firefox, Safari.
* **Безопасность:** Запускается от имени пользователя `nobody` с жесткими лимитами CPU и ОЗУ на уровне systemd.

### Установка

Инструкции по установке как systemd-юнита описаны выше в разделе [Installation & Setup](#-installation--setup-linux-systemd). Вы также можете легко поменять целевой объем трафика в сутки (в гигабайтах), изменив переменную `TARGET_GB_PER_DAY` внутри скрипта `traffic_noise.py`.

### Лицензия
MIT License.
