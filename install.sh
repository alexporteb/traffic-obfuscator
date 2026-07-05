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
mkdir -p "${INSTALL_DIR}"
curl -sSL https://raw.githubusercontent.com/alexporteb/traffic-obfuscator/main/traffic_noise.py -o "${SCRIPT_PATH}"
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
systemctl enable --now ${SERVICE_NAME}

echo "Installation complete!"
echo "Check status with: systemctl status ${SERVICE_NAME}"
