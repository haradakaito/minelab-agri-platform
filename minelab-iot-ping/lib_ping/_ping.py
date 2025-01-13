import time
from datetime import datetime, timedelta
import ping3

class Ping:
    def __init__(self) -> None:
        ping3.EXCEPTIONS = True
        self.success_count = 0
        self.failure_count = 0

    def send(self, destination: str):
        """Pingを送信する関数"""
        try:
            result = ping3.ping(self)
            if result is not None:
                self.success_count += 1
            else:
                self.failure_count += 1
        except ping3.errors.Timeout:
            self.failure_count += 1

    def display_results(self):
        """Pingの結果を表示する関数"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Total Ping: {self.success_count + self.failure_count}, Successful: {self.success_count}, Failed: {self.failure_count}")