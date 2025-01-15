#!/bin/bash

# === 更新の実行 ===
echo "1. システムのupdateを行います..."
sudo apt update && sudo apt upgrade -y
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
echo "pipのupdateが完了しました。"

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
pip3 install --upgrade pyOpenSSL cryptography
pip3 install --upgrade botocore
echo "pyOpenSSL、cryptography、botocoreのアップグレードが完了しました。"

# === Cronの有効化と起動確認 ===
echo "6. Cronの有効化と起動確認を行います..."
sudo systemctl enable cron  # 自動起動を有効化
if systemctl is-active --quiet cron; then
  echo "cronはすでにアクティブです。"
else
  echo "cronが停止しているため起動します..."
  sudo systemctl start cron
  echo "cronのサービスを起動しました。"
fi

# === Cron設定の追加 ===
echo "7. Cronの設定を追加します..."
CRON_CONFIG_PATH="/home/pi/minelab-agri-platform/minelab-iot-camera/__init__/setup-config.yaml"
CRON_ENTRY=$(grep "upload_image:" "$CRON_CONFIG_PATH" | awk -F': ' '{print $2}' | xargs)

if [ -n "$CRON_ENTRY" ]; then
  # crontabへの追加(重複しないように一旦削除して追加)
  (crontab -l | grep -v "$CRON_ENTRY"; echo "$CRON_ENTRY") | crontab -
  echo "Cronジョブの設定を行いました: $CRON_ENTRY"
else
  echo "Error: setup-config.yaml 内のCron情報が見つかりません。"
  exit 1
fi

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