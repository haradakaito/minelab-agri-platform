#!/bin/bash

# YAMLファイルのパス
YAML_FILE="setup-config.yaml"

# cron設定ファイル
TEMP_CRON_FILE="/tmp/cron_temp"

# cronサービスの有効化と起動
echo "cronサービスを有効化し、起動します..."
sudo systemctl enable cron
sudo systemctl start cron

# 既存のcronジョブをバックアップ
echo "既存のcronジョブをバックアップしています..."
crontab -l > $TEMP_CRON_FILE.bak 2>/dev/null

# cronジョブを追加
echo "YAMLファイル $YAML_FILE からcronジョブを追加します..."

# YAMLファイルから`schedule`と`command`を取得
SCHEDULE=$(grep "schedule:" $YAML_FILE | awk '{print $2}')
COMMAND=$(grep "command" $YAML_FILE | sed -e 's/.*command *: *//')

# 同じコマンドの重複を防ぐため、既存のcron設定から同じコマンドを削除
grep -v "$COMMAND" $TEMP_CRON_FILE > "${TEMP_CRON_FILE}_new"
mv "${TEMP_CRON_FILE}_new" $TEMP_CRON_FILE

# 新しいcronジョブを追加
echo "新しいジョブを追加: $SCHEDULE $COMMAND"
echo "$SCHEDULE $COMMAND" >> $TEMP_CRON_FILE

# crontabを更新
crontab $TEMP_CRON_FILE

echo "cronジョブを正常に追加しました。"

# サービスステータスを確認
echo "cronサービスのステータスを確認しています..."
sudo systemctl status cron | grep "Active:"