# 使用方法

## CSIエクスプローラーの起動

- csichanger/pcapディレクトリ直下に，任意のpcapファイルを置いておく

```
$ cd ~
$ git clone https://github.com/haradakaito/minelab-agri-platform.git
$ cd minelab-agri-platform/csichanger/
$ python csichanger.py

// "ファイル名を入力してください："と表示されるので，任意のファイル名を入力
// csvディレクトリ下に振幅データ（csv/amp/*.pcap）と位相データ（csv/pha/*.pcap）が出力される
```

## 実際の実行例

```
$ python csichanger.py
ファイル名を入力してください：_sample.pcap
データの読み込みを開始します
データの抽出を開始します
データの保存を開始します
変換が完了しました
振幅データ：csv/amp/_sample.csv
位相データcsv/pha/_sample.csv
```

## 参考元

CSI Explorer：https://github.com/nexmonster/nexmon_csi/tree/feature/python/utils/python
