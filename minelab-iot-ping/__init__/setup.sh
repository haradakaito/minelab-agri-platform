#!/bin/bash

# === 更新の実行 ===
echo "1. システムのupdateを行います..."
sudo apt update -y
sudo apt upgrade -y
echo "システムのupdateが完了しました。"

# === pipのupdate ===
echo "2. pipのupdateを行います..."
python3 -m pip install --upgrade pip

# === requirements.txtのパッケージインストール ===
REQUIREMENTS_PATH="/home/pi/minelab-agri-platform/minelab-iot-ping/requirements.txt"
echo "3. requirements.txtのパッケージをインストールします..."
if [ -f "$REQUIREMENTS_PATH" ]; then
  pip3 install -r "$REQUIREMENTS_PATH"
  echo "パッケージのインストールが完了しました。"
else
  echo "Error: $REQUIREMENTS_PATH が見つかりません。"
  exit 1
fi

# === Cronの有効化と起動確認 ===
echo "4. Cronの有効化と起動確認を行います..."
sudo systemctl enable cron  # 自動起動を有効化
if ! systemctl is-active --quiet cron; then
  echo "cronが停止しているため起動します..."
  sudo systemctl start cron
fi

echo "cronのサービスは正常に動作しています。"

# === setup-config.yaml の Cron 設定を適用 ===
echo "5. setup-config.yaml の Cron 設定を適用します..."
CRON_CONFIG_PATH="/home/pi/minelab-agri-platform/minelab-iot-ping/__init__/setup-config.yaml"

if [ ! -f "$CRON_CONFIG_PATH" ]; then
  echo "Error: setup-config.yaml が見つかりません。"
  exit 1
fi

# Cronジョブを取得
SEND_PING=$(grep "send_ping:" "$CRON_CONFIG_PATH" | awk -F': ' '{print $2}' | xargs)

if [ -z "$SEND_PING" ] || [ -z "$UPDATE_CONFIG" ]; then
  echo "Error: setup-config.yaml からCron情報を正しく取得できませんでした。"
  exit 1
fi

# 現在のcrontabをバックアップし、新しいcrontabを設定
TMP_CRON=$(mktemp)
crontab -l 2>/dev/null | grep -v -E "$SEND_PING|$UPDATE_CONFIG" > "$TMP_CRON"
echo "$SEND_PING" >> "$TMP_CRON"
echo "$UPDATE_CONFIG" >> "$TMP_CRON"
crontab "$TMP_CRON"
rm "$TMP_CRON"

echo "Cronジョブの設定を更新しました。"

# === Cron設定の確認 ===
echo "=========================================="
echo "現在のCronジョブ設定を確認します..."
echo "------------------------------------------"
crontab -l
echo "=========================================="

# === 再起動メッセージの出力 ===
echo "=========================================="
echo "システム更新が完了しました。"
echo "再起動を行ってください。"
echo "再起動コマンド: sudo reboot"
echo "=========================================="