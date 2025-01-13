import os
import uuid
import socket
import base64
from datetime import datetime
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

    @staticmethod
    def get_device_name() -> str:
        """デバイス名を取得する関数"""
        try:
            device_name = socket.gethostname()
            return device_name
        except Exception as e:
            raise ValidationError("デバイス名の取得に失敗しました") from e

    @staticmethod
    def get_timestamp() -> str:
        """タイムスタンプを取得する関数（ISO8601フォーマットに準拠）"""
        try:
            timestamp = datetime.now().isoformat('T', 'seconds')
            return timestamp
        except Exception as e:
            raise ValidationError("タイムスタンプの取得に失敗しました") from e

    @staticmethod
    def encode_base64(data: bytes) -> str:
        """バイナリデータをBase64エンコードする関数"""
        try:
            encoded_data = base64.b64encode(data).decode('utf-8')
            return encoded_data
        except Exception as e:
            raise ValidationError("Base64エンコードに失敗しました") from e

# 使用例
if __name__ == "__main__":
    try:
        # MACアドレスを取得
        mac_address = Util.get_mac_address()
        print("MAC Address:", mac_address)
        # ルートディレクトリを取得
        root_dir = Util.get_root_dir()
        print("Root Directory:", root_dir)
        # タイムスタンプを取得
        timestamp = Util.get_timestamp()
        print("Timestamp:", timestamp)
        # デバイス名を取得
        device_name = Util.get_device_name()
        print("Device Name:", device_name)
    except Exception as e:
        print(e)
else:
    from lib.custom_error import ValidationError