import time
from datetime import datetime
import ping3

class Ping:
    """Pingを送信するクラス"""
    def __init__(self) -> None:
        ping3.EXCEPTIONS = True
        self.success_count = 0
        self.failure_count = 0

    def send(self, destination: str, timeout: int) -> None:
        """Pingを送信する関数"""
        try:
            result = ping3.ping(destination, timeout=timeout)
            if result is not None:
                self.success_count += 1
            else:
                self.failure_count += 1
        except ping3.errors.Timeout:
            self.failure_count += 1

    def display_results(self) -> None:
        """Pingの結果を表示する関数"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Total Ping: {self.success_count + self.failure_count}, Successful: {self.success_count}, Failed: {self.failure_count}")

# 使用例
if __name__ == "__main__":
    import time

    ping = Ping()
    try:
        while True:
            ping.send(destination="8.8.8.8", timeout=1)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Pingを終了します")
    finally:
        ping.display_results()