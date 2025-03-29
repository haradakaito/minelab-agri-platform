# セットアップ手順

## （推奨）公開鍵によるSSH接続設定

- 有線SSH接続を推奨（Nexmonインストール後は無線が使用できなくなるため）

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
interface eth0
static ip_address=192.168.25.3/22
static routers=192.168.25.1
static domain_name_servers=192.168.25.1

$ sudo reboot
```

## Nexmonのインストール

- 【Raspberry Pi】Nexmon環境構築手順：https://qiita.com/haradakaito/items/8e9ef1081b372509d4a1

```
// 明示的に再起動することを推奨
$ sudo reboot

$ sudo curl -fsSL https://raw.githubusercontent.com/nexmonster/nexmon_csi_bin/main/install.sh | sudo bash
$ sudo reboot
```