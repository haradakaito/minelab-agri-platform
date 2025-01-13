#!/bin/bash

# スクリプト自身のディレクトリを取得
SCRIPT_DIR=$(cd "$(dirname "$0")"; pwd)

# クローン先をスクリプトのあるディレクトリに設定
TARGET_DIR="$SCRIPT_DIR/minelab-agri-platform"
REPO_URL="https://github.com/haradakaito/minelab-agri-platform.git"
SPARSE_DIR="minelab-iot-camera" # スパースチェックアウトするディレクトリ
BRANCH="main"

# クローン処理関数
clone_repository() {
  echo "リポジトリを $TARGET_DIR にクローンします..."
  git clone --filter=blob:none --no-checkout "$REPO_URL" "$TARGET_DIR"
  
  if [ $? -ne 0 ]; then
    echo "エラー: リポジトリのクローンに失敗しました．スクリプトを終了します．"
    exit 1
  fi

  cd "$TARGET_DIR" || exit
  git sparse-checkout init --cone
  git sparse-checkout set "$SPARSE_DIR"
  git checkout "$BRANCH"
  
  if [ $? -eq 0 ]; then
    echo "リポジトリをクローンしました．"
  else
    echo "エラー: チェックアウトに失敗しました．"
    exit 1
  fi
}

# 更新処理関数
update_repository() {
  echo "既にディレクトリ $TARGET_DIR が存在します．更新を行います..."
  cd "$TARGET_DIR" || exit

  # クリーンアップ（必要ならコメント解除）
  # git reset --hard

  git pull origin "$BRANCH"
  
  if [ $? -eq 0 ]; then
    echo "リポジトリを更新しました．"
  else
    echo "エラー: リポジトリの更新に失敗しました．"
    exit 1
  fi
}

# メイン処理
if [ ! -d "$TARGET_DIR" ]; then
  clone_repository
else
  update_repository
fi


# pipのアップデート
echo "pipをアップデートします..."
pip install --upgrade pip
echo "pipのアップデートが完了しました．"

# requirements.txt が存在する場合はインストール
if [ -f "$TARGET_DIR/$SPARSE_DIR/requirements.txt" ]; then
  echo "必要なパッケージをインストールします..."
  pip install -r "$TARGET_DIR/$SPARSE_DIR/requirements.txt"
  echo "パッケージのインストールが完了しました．"
fi

# cronの設定
echo "cronの設定を行います..."
# 30分毎にupdate_image.pyを実行
(crontab -l ; echo "*/30 * * * * python3 $TARGET_DIR/$SPARSE_DIR/update_image.py") | crontab -  # 既存のcronに追記
echo "cronの設定が完了しました．"