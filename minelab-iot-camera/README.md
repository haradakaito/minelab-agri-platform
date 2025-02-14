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
static ip_address=172.16.15.220/22
static routers=172.16.14.1
static domain_name_servers=172.16.15.24

$ sudo reboot
```

## 峰野研究室IoTカメラのセットアップ

```
$ cd ~
$ git clone https://github.com/haradakaito/minelab-agri-platform.git
$ cd minelab-agri-platform/minelab-iot-camera/__init__
$ chmod +x setup.sh
$ bash setup.sh
$ sudo reboot
```

```
$ cd ~/minelab-agri-platform/minelab-iot-camera/config
$ sudo nano device-config.yaml

# project_nameに任意のプロジェクト名を入力

$ sudo nano iam-config.json

# IAM情報（アクセスキー，シークレットキー，APIキー）を入力

$ cd ~/minelab-agri-platform/minelab-iot-camera
$ python encrypt_iam-config.py
```