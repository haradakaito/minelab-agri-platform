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
static ip_address=172.16.15.228/22
static routers=172.16.14.1
static domain_name_servers=172.16.15.24

interface eth0
static ip_address=192.168.25.2/22
static domain_name_servers=192.168.25.1

$ sudo reboot
```

## 初期設定用シェルスクリプトの実行

```
$ cd ~
$ git clone https://github.com/haradakaito/minelab-agri-platform.git
$ cd ~/minelab-agri-platform/minelab-iot-gateway/__init__
$ chmod +x setup.sh
$ bash setup.sh
$ sudo reboot
```

## 設定ファイルの記入・暗号化

```
$ cd ~/minelab-agri-platform/minelab-iot-gateway/config
$ sudo nano config.json

# 全てのパラメータを入力する

$ cd ~/minelab-agri-platform/minelab-iot-gateway
$ python encrypt_config.py
```

## 公開鍵認証

```
$ cd ~
$ ssh-keygen

# 全て何も入力せずにエンター

$ cat .ssh/id_rsa.pub

# 出力された文字列をコピー
# クライアントデバイスそれぞれに対してSSHを行い，以下の操作を実行

(remote)$ cd ~
(remote)$ sudo nano .ssh/authorized_keys

# コピーした公開鍵を追記

(remote)$ sudo reboot
```