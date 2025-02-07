import os
from lib import BaseCustomError, ErrorHandler, ConfigLoader, Util

if __name__ == '__main__':
    try:
        # デバイス設定を取得
        device_config = ConfigLoader(config_path=f'{Util.get_root_dir()}/config/device-config.yaml')
    except BaseCustomError as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/error-{os.path.splitext(os.path.basename(__file__))[0]}.log')
        handler.handle_error(e)