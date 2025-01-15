# セットアップ手順

## SSHキーによるSSH接続設定

```
$ cd ~
$ sudo mkdir .ssh
$ sudo touch ./.ssh/authorized_keys
$ sudo nano ./.ssh/authorized_keys

# 任意のSSHキーを張り付ける
# ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCaWC3pdSsWX4OnYUzkmtYQv1L/vPeQKcT6p1RcoyNZtFhHL6na34Cs2zQWU7mSakWNDgBgoSSFjfVEveJGD2p1D2RdQ88XzwDexW9Q8jY4TtUaXuWkANiCS1BXHs2byej3Xx+IdIxVeDt327j8qZhuZAwryVMXMkAXg3ikzVmUB5L1PhU4LUGsVnJXVHxhFG86twoHyz9suuPhNkvlnk39yJsGjZOUvehLmFfYQaFrwKZ/1GrQpwZBqqkRlXlaIfn5ZQpn35aTnt8S6jZ2ygyQ+V5FS3Susj04h+iORlvlZR0nXwaOM0PnaDXAoLx98hEnRcHiCGiu1WuekUxqS12svEjRyprf+o2klGXmkWa3H/yKXaWtf6PKB0Dt43CaDLIpso+qyefDSNCRJLl6pcMNMdsdlQnJxm8FheS93cVRODA5VRS1200JA0IvShb19r0aAHiMUPA/cTtbiK+goknGrbpA/K0yPExuxc/9NcnPIoWgcAMEMjxZEPYZcSGJXb8= mkrk1@HARADA

$ sudo reboot
```

## IP固定

```
$ sudo nano /etc/dhcpcd.conf

# 以下のフォーマットで末尾に張り付ける
## interface wlan0
## static ip_address=172.16.15.220/22
## static routers=172.16.14.1
## static domain_name_servers=172.16.15.24

$ sudo reboot
```

## 峰野研究室IoTカメラのセットアップ

```
$ cd ~
$ git clone https://github.com/haradakaito/minelab-agri-platform.git
$ cd minelab-agri-platform/minelab-iot-ping/__init__
$ chmod +x setup.sh
$ bash setup.sh
$ sudo reboot
```

```
$ cd ~/minelab-agri-platform/minelab-iot-ping/config
$ sudo nano device-config.yaml

# project_nameに任意のプロジェクト名を入力

$ sudo nano iam-config.json

# IAM情報（アクセスキー，シークレットキー，APIキー）を入力

$ cd ~/minelab-agri-platform/minelab-iot-ping
$ python encrypt_iam-config.py
```