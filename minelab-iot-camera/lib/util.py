import uuid
from pathlib import Path

class Util:
    @staticmethod
    def get_mac_address() -> str:
        """MACアドレスを取得する関数"""
        try:
            mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0, 8*6, 8)][::-1])
            return mac_address
        except Exception as e:
            raise ValidationError("MACアドレスの取得に失敗しました") from e

    @staticmethod
    def get_root_dir() -> Path:
        """プロジェクトのルートディレクトリを取得する関数"""
        try:
            root_dir = Path(__file__).resolve().parent.parent
            return root_dir
        except Exception as e:
            raise ValidationError("ルートディレクトリの取得に失敗しました") from e

# 使用例
if __name__ == "__main__":
    from custom_error import ValidationError, ErrorHandler, BaseCustomError

    try:
        mac_address = Util.get_mac_address()
        print("MAC Address:", mac_address)

        root_dir = Util.get_root_dir()
        print("Root Directory:", root_dir)
    except BaseCustomError as e:
        handler = ErrorHandler(log_file='../log/test-util.log')
        handler.handle_error(e)
else:
    from lib.custom_error import ValidationError