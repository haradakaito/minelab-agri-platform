#!/bin/bash

# === システムの更新 ===
echo "1. システムのupdateを行います..."
sudo apt update -y
echo "システムのupdateが完了しました。"

# === setup-config.yaml の読み込み ===
echo "3. setup-config.yamlを読み込みます..."
CRON_CONFIG_PATH="/home/pi/minelab-agri-platform/minelab-iot-nexmon/__init__/setup-config.yaml"

if [ ! -f "$CRON_CONFIG_PATH" ]; then
  echo "Error: setup-config.yaml が見つかりません。"
  exit 1
fi

MCP_PARAM=$(grep "mcp_param:" "$CRON_CONFIG_PATH" | awk -F': ' '{print $2}' | xargs)

# === Nexmon スクリプトの設定 ===
echo "4. Nexmonの設定を行います..."
NEXMON_SCRIPT="/usr/local/bin/nexmon_start.sh"
NEXMON_SERVICE="/etc/systemd/system/nexmon_start.service"

# Nexmon起動スクリプトを作成
echo "#!/bin/bash
ifconfig wlan0 up
sleep 2
nexutil -Iwlan0 -s500 -b -l34 -v$MCP_PARAM
sleep 1
iw dev wlan0 interface add mon0 type monitor
sleep 1
ip link set mon0 up
sleep 1
exit 0" | sudo tee "$NEXMON_SCRIPT" > /dev/null

# 実行権限を追加
sudo chmod +x "$NEXMON_SCRIPT"
echo "Nexmon起動スクリプトを作成しました。"

# Nexmon サービスを作成
echo "[Unit]
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
WantedBy=multi-user.target" | sudo tee "$NEXMON_SERVICE" > /dev/null

# サービスの設定と起動
echo "5. Nexmon サービスを設定および起動します..."
sudo systemctl daemon-reload
sudo systemctl enable nexmon_start.service
sudo systemctl start nexmon_start.service

# ステータスの確認
echo "=========================================="
echo "Nexmon サービスのステータス:"
sudo systemctl status nexmon_start.service --no-pager

# === 不要なディレクトリの削除 ===
echo "6. minelab-iot-nexmon 以外のディレクトリを削除します..."

TARGET_DIR="/home/pi/minelab-agri-platform"
EXCLUDE_DIR="minelab-iot-nexmon"

# 指定ディレクトリ以下のサブディレクトリをチェックして削除
for dir in "$TARGET_DIR"/*; do
  if [ -d "$dir" ] && [ "$(basename "$dir")" != "$EXCLUDE_DIR" ]; then
    echo "削除: $dir"
    rm -rf "$dir"
  fi
done

echo "不要なディレクトリの削除が完了しました。"

echo "=========================================="
echo "すべての設定が完了しました。システムの再起動を行ってください。"
echo "再起動コマンド: sudo reboot"
echo "=========================================="