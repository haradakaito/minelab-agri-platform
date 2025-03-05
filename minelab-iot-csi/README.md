# セットアップ手順

## （推奨）公開鍵によるSSH接続設定

```
$ cd ~
$ sudo mkdir .ssh
$ sudo touch ./.ssh/authorized_keys
$ sudo nano ./.ssh/authorized_keys

# 任意の公開鍵（.pub）を追記

$ sudo reboot
```

## 初期設定用シェルスクリプトの実行

```
$ cd ~
$ git clone https://github.com/haradakaito/minelab-agri-platform.git
$ cd minelab-agri-platform/minelab-iot-csi/__init__
$ chmod +x setup.sh
$ bash setup.sh
$ sudo reboot
```

## 設定ファイルの記入・暗号化

```
$ cd ~/minelab-agri-platform/minelab-iot-csi/config
$ sudo nano config.json

# 全てのパラメータを入力する

$ cd ~/minelab-agri-platform/minelab-iot-csi
$ python encrypt_config.py
```