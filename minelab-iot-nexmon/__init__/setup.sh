#!/bin/bash

# === YAMLファイルの読み込みとコマンドの実行 ===
YAML_FILE="/home/pi/minelab-agri-platform/minelab-iot-camera/setup-config.yaml"

echo "1. YAMLファイルを読み込みます: $YAML_FILE"
if [ ! -f "$YAML_FILE" ]; then
    echo "Error: $YAML_FILE が見つかりません。"
    exit 1
fi

# YAMLファイルからパラメータを取得
CHANNEL=$(grep "channel:" "$YAML_FILE" | awk '{print $2}')
BANDWIDTH=$(grep "bandwidth:" "$YAML_FILE" | awk '{print $2}')
MAC=$(grep "mac:" "$YAML_FILE" | awk '{print $2}')

echo "観測チャンネル: $CHANNEL"
echo "帯域幅: $BANDWIDTH"
echo "フィルタリングMAC: $MAC"

# コマンドの実行
echo "2. コマンドを順次実行します..."

# mcp コマンドを実行して結果を取得
MCP_CMD=$(grep '"mcp":' "$YAML_FILE" | awk -F'"' '{print $4}')
if [ -n "$MCP_CMD" ]; then
    echo "実行: $MCP_CMD -c $CHANNEL/$BANDWIDTH -m $MAC"
    MCP_OUTPUT=$(sudo $MCP_CMD -c $CHANNEL/$BANDWIDTH -m $MAC)
else
    echo "Error: MCPコマンドが見つかりません。"
    exit 1
fi

# ifconfig コマンドの実行
IFCONFIG_CMD=$(grep '"ifconfig":' "$YAML_FILE" | awk -F'"' '{print $4}')
if [ -n "$IFCONFIG_CMD" ]; then
    echo "実行: $IFCONFIG_CMD"
    sudo $IFCONFIG_CMD
else
    echo "Warning: ifconfig コマンドが見つかりません。"
fi

# iw コマンドの実行
IW_CMD=$(grep '"iw":' "$YAML_FILE" | awk -F'"' '{print $4}')
if [ -n "$IW_CMD" ]; then
    echo "実行: $IW_CMD"
    sudo $IW_CMD
else
    echo "Warning: iw コマンドが見つかりません。"
fi

# ip コマンドの実行
IP_CMD=$(grep '"ip":' "$YAML_FILE" | awk -F'"' '{print $4}')
if [ -n "$IP_CMD" ]; then
    echo "実行: $IP_CMD"
    sudo $IP_CMD
else
    echo "Warning: ip コマンドが見つかりません。"
fi

# nexutil コマンドの実行（MCPの出力を引数に追加）
NEXUTIL_CMD=$(grep '"nexutil":' "$YAML_FILE" | awk -F'"' '{print $4}')
if [ -n "$NEXUTIL_CMD" ]; then
    echo "実行: $NEXUTIL_CMD $MCP_OUTPUT"
    sudo $NEXUTIL_CMD "$MCP_OUTPUT"
else
    echo "Warning: nexutil コマンドが見つかりません。"
fi

# === Cronの有効化と起動確認 ===
echo "3. Cronの有効化と起動確認を行います..."
sudo systemctl enable cron
if systemctl is-active --quiet cron; then
    echo "cronはすでにアクティブです。"
else
    echo "cronが停止しているため起動します..."
    sudo systemctl start cron
    echo "cronのサービスを起動しました。"
fi

# === Cron設定の追加 ===
echo "4. Cronの設定を追加します..."
CRON_CONFIG_PATH="/home/pi/minelab-agri-platform/minelab-iot-camera/setup-config.yaml"
CRON_ENTRY=$(grep "upload_image:" "$CRON_CONFIG_PATH" | awk -F': ' '{print $2}' | xargs)

if [ -n "$CRON_ENTRY" ]; then
    (crontab -l | grep -v "$CRON_ENTRY"; echo "$CRON_ENTRY") | crontab -
    echo "Cronジョブの設定を行いました: $CRON_ENTRY"
else
    echo "Warning: setup-config.yaml 内のCron情報が見つかりません。"
fi

# === Pcap取得スクリプトのCron設定 ===
PCAP_CRON_ENTRY=$(grep "get_pcap:" "$YAML_FILE" | awk -F': ' '{print $2}' | xargs)

if [ -n "$PCAP_CRON_ENTRY" ]; then
    echo "Cronジョブを追加します: $PCAP_CRON_ENTRY"
    (crontab -l | grep -v "$PCAP_CRON_ENTRY"; echo "$PCAP_CRON_ENTRY") | crontab -
    echo "Pcap取得スクリプトのCronジョブを設定しました: $PCAP_CRON_ENTRY"
else
    echo "Warning: get_pcapのCron情報が見つかりません。"
fi

# === Cron設定の確認 ===
echo "=========================================="
echo "現在のCronジョブ設定を確認します..."
echo "------------------------------------------"
crontab -l
echo "=========================================="

# === 再起動メッセージの出力 ===
echo "=========================================="
echo "システム更新とコマンド実行が完了しました。"
echo "再起動を行ってください。"
echo "再起動コマンド: sudo reboot"
echo "=========================================="