#!/bin/bash

# === 更新の実行 ===
echo "1. システムのupdateを行います..."
sudo apt update -y
echo "システムのupdateが完了しました。"

# === python3-opencvのインストール ===
echo "2. python3-opencvをインストールします..."
if dpkg -l | grep -q "python3-opencv"; then
  echo "python3-opencvはすでにインストールされています。"
else
  sudo apt install -y python3-opencv
  echo "python3-opencvのインストールが完了しました。"
fi

# === pipのupdate ===
echo "3. pipのupdateを行います..."
python3 -m pip install --upgrade pip

# === requirements.txtのパッケージインストール ===
REQUIREMENTS_PATH="/home/pi/minelab-agri-platform/minelab-iot-camera/requirements.txt"
echo "4. requirements.txtのパッケージをインストールします..."
if [ -f "$REQUIREMENTS_PATH" ]; then
  pip3 install -r "$REQUIREMENTS_PATH"
  echo "パッケージのインストールが完了しました。"
else
  echo "Error: $REQUIREMENTS_PATH が見つかりません。"
  exit 1
fi

# === 特定パッケージのアップグレード ===
echo "5. 必要なパッケージ(pyOpenSSL, cryptography, botocore)のアップグレードを行います..."
pip3 install --upgrade pyOpenSSL cryptography botocore

echo "パッケージのアップグレードが完了しました。"

# === Cronの有効化と起動確認 ===
echo "6. Cronの有効化と起動確認を行います..."
sudo systemctl enable cron  # 自動起動を有効化
if ! systemctl is-active --quiet cron; then
  echo "cronが停止しているため起動します..."
  sudo systemctl start cron
fi

echo "cronのサービスは正常に動作しています。"

# === setup-config.yaml の Cron 設定を適用 ===
echo "7. setup-config.yaml の Cron 設定を適用します..."
CRON_CONFIG_PATH="/home/pi/minelab-agri-platform/minelab-iot-camera/__init__/setup-config.yaml"

if [ ! -f "$CRON_CONFIG_PATH" ]; then
  echo "Error: setup-config.yaml が見つかりません。"
  exit 1
fi

# Cronジョブを取得
UPLOAD_IMAGE=$(grep "upload_image:" "$CRON_CONFIG_PATH" | awk -F': ' '{print $2}' | xargs)
UPDATE_CONFIG=$(grep "update_config:" "$CRON_CONFIG_PATH" | awk -F': ' '{print $2}' | xargs)

if [ -z "$UPLOAD_IMAGE" ] || [ -z "$UPDATE_CONFIG" ]; then
  echo "Error: setup-config.yaml からCron情報を正しく取得できませんでした。"
  exit 1
fi

# 現在のcrontabをバックアップし、新しいcrontabを設定
TMP_CRON=$(mktemp)
crontab -l 2>/dev/null | grep -v -E "$UPLOAD_IMAGE|$UPDATE_CONFIG" > "$TMP_CRON"
echo "$UPLOAD_IMAGE" >> "$TMP_CRON"
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

# === 不要なディレクトリの削除 ===
echo "8. minelab-iot-camera 以外のディレクトリを削除します..."

TARGET_DIR="/home/pi/minelab-agri-platform"
EXCLUDE_DIR="minelab-iot-camera"

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