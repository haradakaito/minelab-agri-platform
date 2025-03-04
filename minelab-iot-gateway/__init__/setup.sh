#!/bin/bash

# === 更新の実行 ===
echo "1. システムのupdateを行います..."
sudo apt update -y
echo "システムのupdateが完了しました。"

# === pipのupdate ===
echo "2. pipのupdateを行います..."
python3 -m pip install --upgrade pip

# === requirements.txtのパッケージインストール ===
REQUIREMENTS_PATH="/home/pi/minelab-agri-platform/minelab-iot-gateway/requirements.txt"
echo "3. requirements.txtのパッケージをインストールします..."
if [ -f "$REQUIREMENTS_PATH" ]; then
  pip3 install -r "$REQUIREMENTS_PATH"
  echo "パッケージのインストールが完了しました。"
else
  echo "Error: $REQUIREMENTS_PATH が見つかりません。"
  exit 1
fi

# === 特定パッケージのアップグレード ===
echo "4. 必要なパッケージ(pyOpenSSL, cryptography, botocore)のアップグレードを行います..."
pip3 install --upgrade pyOpenSSL cryptography botocore
echo "パッケージのアップグレードが完了しました。"

# === Cronの有効化と起動確認 ===
echo "5. Cronの有効化と起動確認を行います..."
sudo systemctl enable cron  # 自動起動を有効化
if ! systemctl is-active --quiet cron; then
  echo "cronが停止しているため起動します..."
  sudo systemctl start cron
fi
echo "cronのサービスは正常に動作しています。"

# === Cron設定の適用 ===
echo "6. Cronの設定を適用します..."

# 現在のcrontabをバックアップし、新しいcrontabを設定
TMP_CRON=$(mktemp)
crontab -l 2>/dev/null | grep -v -E "update_config|exec_nexmon|get_pcap|delete_pcap|preprocess_csv|upload_csv|delete_csv" > "$TMP_CRON"

echo "0 0 1 * * python3 /home/pi/minelab-agri-platform/minelab-iot-gateway/update_config.py >> /home/pi/minelab-agri-platform/minelab-iot-gateway/log/update_config.log 2>&1" >> "$TMP_CRON"
echo "*/15 * * * * python3 /home/pi/minelab-agri-platform/minelab-iot-gateway/exec_nexmon.py >> /home/pi/minelab-agri-platform/minelab-iot-gateway/log/exec_nexmon.log 2>&1" >> "$TMP_CRON"
echo "0 2 * * * python3 /home/pi/minelab-agri-platform/minelab-iot-gateway/get_pcap.py >> /home/pi/minelab-agri-platform/minelab-iot-gateway/log/get_pcap.log 2>&1" >> "$TMP_CRON"
echo "0 3 * * * python3 /home/pi/minelab-agri-platform/minelab-iot-gateway/upload_pcap.py >> /home/pi/minelab-agri-platform/minelab-iot-gateway/log/upload_pcap.log 2>&1" >> "$TMP_CRON"
echo "0 4 * * * python3 /home/pi/minelab-agri-platform/minelab-iot-gateway/delete_pcap.py >> /home/pi/minelab-agri-platform/minelab-iot-gateway/log/cron-delete_pcap.log 2>&1" >> "$TMP_CRON"
echo "0 4 * * * find /home/pi/minelab-agri-platform/minelab-iot-gateway/pcap -type f -name \"*.pcap\" -delete" >> "$TMP_CRON"

crontab "$TMP_CRON"
rm "$TMP_CRON"

echo "Cronジョブの設定を更新しました。"

# === Cron設定の確認 ===
echo "=========================================="
echo "現在のCronジョブ設定を確認します..."
echo "------------------------------------------"
crontab -l
echo "=========================================="

# === 不要なディレクトリの削除 ===
echo "7. minelab-iot-gateway 以外のディレクトリを削除します..."

TARGET_DIR="/home/pi/minelab-agri-platform"
EXCLUDE_DIR="minelab-iot-gateway"

# 指定ディレクトリ以下のサブディレクトリをチェックして削除
for dir in "$TARGET_DIR"/*; do
  if [ -d "$dir" ] && [ "$(basename "$dir")" != "$EXCLUDE_DIR" ]; then
    echo "削除: $dir"
    rm -rf "$dir"
  fi
done

echo "不要なディレクトリの削除が完了しました。"

# === 再起動メッセージの出力 ===
echo "=========================================="
echo "システム更新が完了しました。"
echo "再起動を行ってください。"
echo "再起動コマンド: sudo reboot"
echo "=========================================="