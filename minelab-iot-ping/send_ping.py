import time
import os
from datetime import datetime, timedelta
from lib import BaseCustomError, ErrorHandler, ConfigLoader, Util
from lib_ping import Ping

if __name__ == '__main__':
    try:
        # Pingオブジェクトの生成
        ping = Ping()

        # デバイス設定の取得
        device_config = ConfigLoader(config_path=f'{Util.get_root_dir()}/config/device-config.yaml')

        # Pingを一定時間だけホストに一定間隔で送信
        start_time = datetime.now()                                                     # 開始時間を設定
        end_time   = start_time + timedelta(seconds=int(device_config.get('duration'))) # 終了時間を設定（開始時間 + duration秒）

        while datetime.now() < end_time:
            # Ping送信（送信先ホストは設定ファイルから取得）
            ping.send(
                destination = str(device_config.get('destination')), # 送信先ホスト
                timeout     = int(device_config.get('timeout'))      # タイムアウト時間
            )
            # インターバル時間だけ待機
            time.sleep(int(device_config.get('interval')))

        # 結果を表示
        ping.display_results()
    except BaseCustomError as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/{os.path.splitext(os.path.basename(__file__))[0]}.log')
        handler.handle_error(e)