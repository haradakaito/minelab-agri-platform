# セットアップ手順

## （推奨）公開鍵によるSSH接続設定

```
$ cd ~
$ mkdir .ssh
$ touch ./.ssh/authorized_keys
$ nano ./.ssh/authorized_keys

# 任意の公開鍵（.pub）を追記

$ sudo reboot
```

## （推奨）IP固定

```
$ sudo nano /etc/dhcpcd.conf

# 以下のフォーマットで末尾に追記
interface wlan0
static ip_address=172.16.15.220/22
static routers=172.16.14.1
static domain_name_servers=172.16.15.24

$ sudo reboot
```

## 初期設定用シェルスクリプトの実行

```
$ cd ~
$ git clone https://github.com/haradakaito/minelab-agri-platform.git
$ cd ~/minelab-agri-platform/minelab-iot-ping/__init__
$ chmod +x setup.sh
$ bash setup.sh
$ sudo reboot
```

## 設定ファイルの記入

```
$ cd ~/minelab-agri-platform/minelab-iot-camera/config
$ sudo nano config.json

# 全てのパラメータを入力して保存
```