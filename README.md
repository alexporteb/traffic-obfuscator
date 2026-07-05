# Proxy Noise Generator 🥷

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)

[🇷🇺 Русская версия](#русская-версия) | [🇬🇧 English version](#english-version)

---

## 🇬🇧 English version

**Proxy Noise Generator** is a lightweight, zero-dependency Python script designed to run as a background systemd service on Linux VPS. It generates randomized background HTTP/HTTPS download traffic to disrupt symmetric In/Out traffic patterns often associated with proxy servers or VPNs.

### 🌟 Features
* **Zero Disk I/O:** Streams data directly to memory and immediately discards it.
* **Zero Dependencies:** Uses only Python's built-in `urllib`.
* **Randomized Patterns:** Randomizes download sizes, intervals, and target URLs.
* **User-Agent Spoofing:** Rotates through a list of modern browser User-Agents.
* **Stealthy:** Runs securely under the unprivileged `nobody` user with systemd-enforced CPU/Memory limits. The service is obfuscated under the generic name `sys-metrics`.

### 🚀 Quick Installation (One-liner)

Run the following command as root (or with sudo) to automatically download, install, and start the service:

```bash
# As root:
curl -sSL https://raw.githubusercontent.com/alexporteb/traffic-obfuscator/main/install.sh | bash

# Or via sudo:
curl -sSL https://raw.githubusercontent.com/alexporteb/traffic-obfuscator/main/install.sh | sudo bash
```

### ⚙️ Configuration
To adjust limits, edit `/opt/sys-metrics/sys_metrics.py` after installation:
* `TARGET_GB_PER_DAY` — Target volume of traffic per day (default: `50.0` GB).
* `SLEEP_MIN_SECONDS` / `SLEEP_MAX_SECONDS` — Minimum and maximum sleep intervals between download sessions.

After editing, restart the service:
```bash
sudo systemctl restart sys-metrics
```

### 🔍 Logs
To view the activity logs:
```bash
sudo journalctl -u sys-metrics -f
```

---

## 🇷🇺 Русская версия

**Proxy Noise Generator** — это легковесный Python-скрипт без зависимостей, предназначенный для работы в фоне на Linux VPS. Он генерирует случайный входящий трафик для размытия симметричного паттерна (соотношения In/Out), характерного для прокси-серверов и VPN.

### 🌟 Особенности
* **Не использует диск:** Скачивает данные в оперативную память и сразу отбрасывает.
* **Без зависимостей:** Использует только встроенную библиотеку `urllib`.
* **Полный рандом:** Случайный выбор файла, объем скачивания и паузы между сессиями.
* **Маскировка (User-Agent):** Подставляет заголовки современных браузеров.
* **Скрытность:** Запускается от пользователя `nobody` с лимитами CPU и ОЗУ. Сервис маскируется под системный процесс с названием `sys-metrics`.

### 🚀 Быстрая установка (Одной командой)

Выполните следующую команду от имени root (или через sudo), чтобы автоматически скачать, установить и запустить сервис:

```bash
# От имени root:
curl -sSL https://raw.githubusercontent.com/alexporteb/traffic-obfuscator/main/install.sh | bash

# Или через sudo:
curl -sSL https://raw.githubusercontent.com/alexporteb/traffic-obfuscator/main/install.sh | sudo bash
```

### ⚙️ Конфигурация
Чтобы изменить лимиты, отредактируйте файл `/opt/sys-metrics/sys_metrics.py` после установки:
* `TARGET_GB_PER_DAY` — Целевой объем трафика в сутки (по умолчанию `50.0` ГБ).
* `SLEEP_MIN_SECONDS` / `SLEEP_MAX_SECONDS` — Минимальный и максимальный интервалы сна.

После редактирования перезапустите сервис:
```bash
sudo systemctl restart sys-metrics
```

### 🔍 Логи
Для просмотра логов работы скрипта:
```bash
sudo journalctl -u sys-metrics -f
```
