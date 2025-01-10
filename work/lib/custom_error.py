import os
import sys
import logging
import traceback
from datetime import datetime

# エラーの基底クラス
class BaseCustomError(Exception):
    """すべてのカスタム例外の基底クラス"""
    def __init__(self, message: str, error_code: int = 1000):
        super().__init__(message)
        self.message    = message     # エラーのメッセージ
        self.error_code = error_code  # エラーコード

    def __str__(self) -> str:
        """エラーの詳細を文字列で返す"""
        return f"[{self.__class__.__name__}] Error Code: {self.error_code}, Message: {self.message}"

# バリデーションエラー
class ValidationError(BaseCustomError):
    """バリデーションエラーを表すクラス"""
    def __init__(self, message: str, error_code: int = 1001):
        super().__init__(message, error_code)

# データベースエラー
class DatabaseError(BaseCustomError):
    """データベースエラーを表すクラス"""
    def __init__(self, message: str, error_code: int = 2001):
        super().__init__(message, error_code)

# APIエラー
class APIError(BaseCustomError):
    """APIエラーを表すクラス"""
    def __init__(self, message: str, error_code: int = 3001):
        super().__init__(message, error_code)

# エラーハンドラー
class ErrorHandler:
    """エラーハンドリングを行うクラス"""
    def __init__(self, log_file: str):
        """ログファイルを指定してエラーハンドラーを初期化"""
        self.log_file = log_file
        # log_fileのパスが存在しない場合は作成
        if not os.path.exists(log_file):
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
        # ログ設定を追加
        logging.basicConfig(
            filename=self.log_file,
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8'
        )

    def log_error(self, error: Exception) -> None:
        """エラーをログファイルに書き込む"""
        error_message = self._format_error_message(error)
        logging.error(error_message)
        print(f"エラーが発生しました: {error_message}")

    def _format_error_message(self, error: Exception) -> str:
        """エラーの詳細を整形して文字列で返す"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # BaseCustomErrorのインスタンスかどうかをチェック
        if isinstance(error, BaseCustomError):
            return f"[{timestamp}] {error}"
        else:
            # 予期しないエラーの場合はトレースバックを含めたメッセージを取得
            traceback_str = traceback.format_exc()
            return f"[{timestamp}] Unexpected Error: {error}\n{traceback_str}"

    def handle_error(self, error: Exception) -> None:
        """エラーを処理するメソッド"""
        self.log_error(error)
        sys.exit(1)

# 使用例
if __name__ == '__main__':
    try:
        raise ValidationError("バリデーションエラーが発生しました")
    except BaseCustomError as e:
        handler = ErrorHandler(log_file='../log/test-custom_error.log')
        handler.handle_error(e)
