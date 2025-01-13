# 峰野研究室IoTプラットフォーム開発

峰野研究室のIoTプラットフォーム開発に関するリポジトリです．

## インストール・セットアップ方法

```
# __init__のinstall-config.yamlとinstall.shを各種IoTデバイスの/home/pi/下に置く
# install-config.yamlのdevice_typeのバリューにデバイスタイプを入力する
# デバイスタイプ例：minelab-iot-camera，minelab-iot-nexmon，minelab-iot-pingなど

$ cd ~
$ bash install.sh
$ cd minelab-agri-platform/{minelab-iot-XXXX(install-config.yamlに入力したデバイスタイプ)}/__init__

# setup-config.yamlはデフォルトで基本OK

$ bash setup.sh
```

## API利用方法

```
# 事前にIAM認証キー（iam-config.json）をconfigディレクトリ下に置く必要がある
# APIリクエストのサンプルコード(_sample_api_request.py)実行

$ cd ~
$ cd minelab-agri-platform/minelab-iot-XXXX/
$ python _sample_api_request.py
```