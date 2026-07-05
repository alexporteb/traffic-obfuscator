#!/bin/bash
set -e

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (or use sudo)"
  exit 1
fi

SERVICE_NAME="sys-metrics"
INSTALL_DIR="/opt/${SERVICE_NAME}"
SCRIPT_PATH="${INSTALL_DIR}/sys_metrics.py"

echo "Installing ${SERVICE_NAME}..."

if systemctl is-active --quiet ${SERVICE_NAME}; then
  echo "Stopping existing service..."
  systemctl stop ${SERVICE_NAME}
fi

mkdir -p "${INSTALL_DIR}"
# Use a cache-buster query parameter to bypass GitHub Raw cache
curl -sSL "https://raw.githubusercontent.com/alexporteb/traffic-obfuscator/main/traffic_noise.py?v=$RANDOM" -o "${SCRIPT_PATH}"
chmod +x "${SCRIPT_PATH}"

cat <<EOF > /etc/systemd/system/${SERVICE_NAME}.service
[Unit]
Description=System Metrics Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
DynamicUser=yes
ExecStart=/usr/bin/python3 ${SCRIPT_PATH}
Restart=always
RestartSec=30
MemoryMax=150M
CPUQuota=20%

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable ${SERVICE_NAME}
systemctl restart ${SERVICE_NAME}

echo "Installation complete!"
echo "Check status with: systemctl status ${SERVICE_NAME}"
