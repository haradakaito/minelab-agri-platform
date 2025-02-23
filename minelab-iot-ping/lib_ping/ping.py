import ping3

class Ping:
    """Pingを送信するクラス"""
    def __init__(self) -> None:
        ping3.EXCEPTIONS = True

    def send(self, destination: str, timeout: int) -> None:
        """Pingを送信する関数"""
        try:
            _ = ping3.ping(destination, timeout=timeout)
        except Exception as e:
            raise e

# 使用例
if __name__ == "__main__":
    try:
        ping = Ping()
        for _ in range(10):
            ping.send(destination="8.8.8.8", timeout=1)
        print("Pingの送信が完了しました")
    except KeyboardInterrupt:
        print("Pingを終了します")