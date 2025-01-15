import os
from lib import ConfigLoader, AESCodec, Util, BaseCustomError, ErrorHandler

if __name__ == "__main__":
    try:
        # 設定ファイルを読み込む
        iam_config = ConfigLoader(config_path=f'{Util.get_root_dir()}/config/iam-config.json') # IAM設定ファイル

        # 設定ファイルを更新
        for key in iam_config.get():
            # 設定ファイルから値を取得
            encrypted_data = AESCodec(key=Util.get_mac_address()).encode(plaintext=iam_config.get(key))                  # 再度暗号化
            # 設定ファイルを更新
            iam_config.set(key, value=encrypted_data)

        # 設定ファイルを保存
        iam_config.save()
    except BaseCustomError as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/error-{os.path.splitext(os.path.basename(__file__))[0]}.log')
        handler.handle_error(e)