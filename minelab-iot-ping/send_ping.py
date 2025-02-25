import time
import json
from datetime import datetime, timedelta
from lib import ErrorHandler, Util
from lib_ping import Ping

if __name__ == '__main__':
    try:
        # 設定ファイルを読み込む
        with open(f"{Util.get_root_dir()}/config/config.json", "r", encoding="utf-8") as file:
            config = json.load(file)

        # Pingオブジェクトの生成
        ping = Ping()
        # Pingを一定時間，一定間隔で送信
        end_time = datetime.now() + timedelta(seconds=int(config["Duration"])) # 終了時間（開始時間 + Duration秒）
        while datetime.now() < end_time:
            try:
                # Ping送信
                ping.send(
                    destination = str(config["Destination"]), # 送信先ホスト
                    timeout     = int(config["Timeout"])      # タイムアウト時間
                )
                # インターバル時間だけ待機
                time.sleep(int(config["Interval"]))

            except Exception as e:
                # エラーハンドラを初期化
                handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/{Util.get_exec_file_name()}.log')
                handler.log_error(e)
                continue
    except Exception as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/{Util.get_exec_file_name()}.log')
        handler.handle_error(e)