# セットアップ手順

## SSHキーによるSSH接続設定

※有線SSH接続を推奨（Nexmonインストール後は無線が使用できなくなるため）

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
interface eth0
static ip_address=192.168.25.3/22
static routers=192.168.25.1
static domain_name_servers=192.168.25.1

$ sudo reboot
```

## 峰野研究室IoTセンサ（Nexmon）のセットアップ

- Nexmonのインストール

```
$ sudo curl -fsSL https://raw.githubusercontent.com/nexmonster/nexmon_csi_bin/main/install.sh | sudo bash
$ sudo reboot
```

※解説記事【Nexmonの環境構築 for RaspberryPi 3/4B】：https://qiita.com/haradakaito/items/8e9ef1081b372509d4a1

- IoTセンサ（Nexmon）の設定

```
$ cd ~
$ git clone https://github.com/haradakaito/minelab-agri-platform.git
$ cd minelab-agri-platform/minelab-iot-nexmon/__init__
$ chmod +x setup.sh
$ bash setup.sh
$ sudo reboot
```