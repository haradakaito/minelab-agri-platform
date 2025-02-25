# 使用方法

## CSIエクスプローラーの起動

- csichanger/pcapfilesディレクトリ直下に，任意のpcapファイルを置いておく

```
$ cd ~
$ git clone https://github.com/haradakaito/minelab-agri-platform.git
$ cd minelab-agri-platform/csichanger/
$ python csiexplorer.py

// "Pcapファイル名："と表示されるので，任意のファイル名を入力
// "空のグラフボックスが表示される"
// ">"に続けて"{開始ID}-{終了ID}"と入力すると，その範囲のCSIデータ（振幅・位相）がアニメーション表示される

// "exit"と入力するとプログラム停止
// "help"と入力するとヘルプメッセージが表示される
```

## 実際のプロット例

```
$ python csiexplorer.py
Pcapファイル名: _sample-80.pcap
> 0-2

Sample #0
---------------
Source Mac ID: 40:ec:99:cc:d9:8b
Sequence: 4095.15
Core and Spatial Stream: 0x0000
RSSI: 17
FCTL: 17


Sample #1
---------------
Source Mac ID: 40:ec:99:cc:d9:8b
Sequence: 3880.0
Core and Spatial Stream: 0x0000
RSSI: 17
FCTL: 17


Sample #2
---------------
Source Mac ID: 40:ec:99:cc:d9:8b
Sequence: 3881.0
Core and Spatial Stream: 0x0000
RSSI: 17
FCTL: 17
```

![動作画面](https://github.com/user-attachments/assets/65d43e30-5da3-4728-93b8-7ff538650ed6)

## 参考元

CSI Explorer：https://github.com/nexmonster/nexmon_csi/tree/feature/python/utils/python
