# セットアップ手順

## SSHキーによるSSH接続設定

```
$ cd ~
$ sudo mkdir .ssh
$ sudo touch ./.ssh/authorized_keys
$ sudo nano ./.ssh/authorized_keys

# 任意のSSHキーを張り付ける

$ sudo reboot
```

## IP固定

```
$ sudo nano /etc/dhcpcd.conf

# 以下のフォーマットで末尾に張り付ける
interface wlan0
static ip_address=172.16.15.228/22
static routers=172.16.14.1
static domain_name_servers=172.16.15.24

interface eth0
static ip_address=192.168.25.2/22
static routers=192.168.25.1
static domain_name_servers=192.168.25.1

$ sudo reboot
```

## 峰野研究室IoTゲートウェイのセットアップ

```
$ cd ~
$ git clone https://github.com/haradakaito/minelab-agri-platform.git
$ cd minelab-agri-platform/minelab-iot-gateway/__init__
$ chmod +x setup.sh
$ bash setup.sh
$ sudo reboot
```

```
$ cd ~/minelab-agri-platform/minelab-iot-gateway/config
$ sudo nano device-config.yaml

# project_nameに任意のプロジェクト名を入力 # 例：csi
# portに22を入力（SSH用ポート番号）
# usernameに任意のユーザー名を入力 # 例：pi
# client_listにクライアントデバイスのホスト名を入力
# remote_pathにクライアントデバイスのリモートパスを入力（pcapファイルの保存場所）

$ sudo nano iam-config.json

# IAM情報（アクセスキー，シークレットキー，APIキー）を入力

$ sudo nano ssh-config.json

# SSH接続情報（パスワード）を入力

$ cd ~/minelab-agri-platform/minelab-iot-gateway
$ python encrypt_iam-config.py
$ python encrypt_ssh-config.py
```