# セットアップ手順

## （推奨）公開鍵によるSSH接続設定

- 有線SSH接続を推奨（Nexmonインストール後は無線が使用できなくなるため）

```
$ cd ~
$ sudo mkdir .ssh
$ sudo touch ./.ssh/authorized_keys
$ sudo nano ./.ssh/authorized_keys

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

## 初期設定用シェルスクリプトの実行

```
$ cd ~
$ git clone https://github.com/haradakaito/minelab-agri-platform.git
$ cd minelab-agri-platform/minelab-iot-nexmon/__init__
$ chmod +x setup.sh
$ bash setup.sh
$ sudo reboot
```

## 

```
$ cd ~
$ sudo nano /usr/local/bin/nexmon_start.sh

# 以下を追記して保存
#!/bin/bash
# ネットワークインターフェースの起動
ifconfig wlan0 up
sleep 2  # インターフェースが完全に起動するまで待つ
# Nexmon の設定
nexutil -Iwlan0 -s500 -b -l34 -v{任意のmcpによって生成されたパラメータ}
sleep 1
# モニターインターフェースの作成
iw dev wlan0 interface add mon0 type monitor
sleep 1
# インターフェースの起動
ip link set mon0 up
sleep 1
exit 0

# 実行権限を追加
$ sudo chmod +x /usr/local/bin/nexmon_start.sh

$ sudo nano /etc/systemd/system/nexmon_start.service

# 以下を追記して保存
[Unit]
Description=Nexmon Startup Script
After=network.target
Wants=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/bin/bash /usr/local/bin/nexmon_start.sh
Restart=on-failure
User=root

[Install]
WantedBy=multi-user.target

# サービスファイルを起動・設定
$ sudo systemctl daemon-reload
$ sudo systemctl enable nexmon_start.service
$ sudo systemctl start nexmon_start.service
$ sudo systemctl status nexmon_start.service

# active (exited)と表示されていれば成功

$ sudo reboot
```