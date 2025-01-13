import time
import sys
from datetime import datetime, timedelta

from lib._ping import Ping

# 定数の定義
DISTINATION = '172.16.14.1' # 送信先アドレス
INTERVAL    = 1             # 1秒間隔で送信
DURATION    = 900           # 900秒間（15分間）送信

# 異常系処理
def handle_error(message: str):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now}] {message}")
    sys.exit(1)

if __name__ == '__main__':
    # Pingのインスタンスを生成
    ping = Ping()
    # Ping送信
    end_time = datetime.now() + timedelta(seconds=DURATION)
    try:
        while datetime.now() < end_time:
            ping.send()
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        handle_error(message="ユーザーによって停止されました")
    except Exception as e:
        handle_error(message=str(e))
    finally:
        # 結果を表示
        ping.display_results()