#!/bin/bash

# === Cron の有効化と起動確認 ===
echo "1. Cron の有効化と起動確認を行います..."
sudo systemctl enable cron  # 自動起動を有効化
if ! systemctl is-active --quiet cron; then
  echo "cron が停止しているため起動します..."
  sudo systemctl start cron
fi
echo "cron のサービスは正常に動作しています。"

# === setup-config.yaml の Cron 設定を適用 ===
CONFIG_FILE="/home/pi/minelab-agri-platform/minelab-iot-ping/__init__/setup-config.yaml"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "Error: setup-config.yaml が見つかりません。"
  exit 1
fi

# 必要なツールがあるか確認
if ! command -v yq &> /dev/null; then
    echo "yq がインストールされていません。インストールします..."
    sudo apt install -y yq
fi

echo "2. setup-config.yaml から設定を読み込みます..."

MCP_PARAM=$(yq '.cron.mcp_param' "$CONFIG_FILE")
DELETE_PCAP=$(yq '.cron.delete_pcap' "$CONFIG_FILE")

if [ -z "$MCP_PARAM" ] || [ -z "$DELETE_PCAP" ]; then
    echo "Error: setup-config.yaml から Cron 情報を正しく取得できませんでした。"
    exit 1
fi

echo ">>> MCP_PARAM: $MCP_PARAM"
echo ">>> DELETE_PCAP: $DELETE_PCAP"

# === Nexmon スタートスクリプトの作成 ===
NEXMON_SCRIPT="/usr/local/bin/nexmon_start.sh"

echo ">>> $NEXMON_SCRIPT を作成中..."
sudo bash -c "cat > $NEXMON_SCRIPT" <<EOF
#!/bin/bash
# ネットワークインターフェースの起動
ifconfig wlan0 up
sleep 2  # インターフェースが完全に起動するまで待つ
# Nexmon の設定
nexutil -Iwlan0 -s500 -b -l34 -v$MCP_PARAM
sleep 1
# モニターインターフェースの作成
iw dev wlan0 interface add mon0 type monitor
sleep 1
# インターフェースの起動
ip link set mon0 up
sleep 1
exit 0
EOF

# 実行権限を付与
echo ">>> 実行権限を付与: $NEXMON_SCRIPT"
sudo chmod +x $NEXMON_SCRIPT

# === systemd サービスファイルの作成 ===
SERVICE_FILE="/etc/systemd/system/nexmon_start.service"

echo ">>> $SERVICE_FILE を作成中..."
sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=Nexmon Startup Script
After=network.target
Wants=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/bin/bash $NEXMON_SCRIPT
Restart=on-failure
User=root

[Install]
WantedBy=multi-user.target
EOF

# systemd の設定
echo ">>> systemd の設定を更新..."
sudo systemctl daemon-reload
sudo systemctl enable nexmon_start.service
sudo systemctl start nexmon_start.service

# サービスの状態を表示
echo ">>> サービスの状態:"
sudo systemctl status nexmon_start.service --no-pager

# === Cron ジョブの設定 ===
echo "3. Cron ジョブの設定を適用します..."
CRON_JOB="$DELETE_PCAP find /home/pi -type f -name \"*.pcap\" -delete"
CRON_FILE="/etc/cron.d/delete_pcap"

echo ">>> Cron ジョブを設定: $CRON_JOB"
echo "$CRON_JOB" | sudo tee "$CRON_FILE" > /dev/null
sudo chmod 644 "$CRON_FILE"
sudo systemctl restart cron

# === Cron 設定の確認 ===
echo "=========================================="
echo "現在の Cron ジョブ設定を確認します..."
echo "------------------------------------------"
crontab -l
echo "=========================================="

# === 再起動メッセージの出力 ===
echo "=========================================="
echo "Nexmon の設定とシステム更新が完了しました。"
echo "再起動を行ってください。"
echo "再起動コマンド: sudo reboot"
echo "=========================================="