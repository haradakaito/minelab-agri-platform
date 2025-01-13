import json
import os

class JsonLoader:
    """構成ファイルを読み込むクラス"""

    def __init__(self, _json_path: str) -> None:
        # 構成ファイルのパスを設定
        self._json_path = _json_path
        # 構成ファイルを読み込み、構成データを取得
        self._json = self._load__json()

    def _load__json(self) -> dict:
        """構成ファイルを読み込む関数"""
        # 構成ファイルが存在しない場合のエラー処理
        if not os.path.exists(self._json_path):
            raise ValidationError(f"構成ファイルが存在しません: {self._json_path}")
        # 構成ファイルを読み込む
        with open(self._json_path, 'r', encoding='utf-8') as file:
            try:
                _json_data = json.load(file)
            except json.JSONDecodeError as e:
                raise ValidationError(f"構成ファイルの読み込みに失敗しました: {e}") from e
        return _json_data

    def get(self, *keys, default=None) -> dict:
        """構成データから値を取得する関数"""
        # 構成データから値を取得
        value = self._json
        try:
            for key in keys:
                value = value[key]
        except (KeyError, TypeError):
            return default
        return value

    def set(self, *keys, value) -> None:
        """構成データに値を設定する関数"""
        # 構成データに値を設定
        try:
            for key in keys[:-1]:
                self._json = self._json.setdefault(key, {})
            self._json[keys[-1]] = value
        except (KeyError, TypeError):
            raise ValidationError(f"構成データの設定に失敗しました: {keys}")

    def save(self) -> None:
        """構成データを保存する関数"""
        # 構成データを保存
        try:
            with open(self._json_path, 'w', encoding='utf-8') as file:
                json.dump(self._json, file, indent=4)
        except Exception as e:
            raise ValidationError(f"構成データの保存に失敗しました: {e}") from e

# 使用例
if __name__ == "__main__":
    from custom_error import BaseCustomError, ValidationError, ErrorHandler

    try:
        _json_loader = JsonLoader(_json_path='../config/iam-images-config.json')
        print(_json_loader.get(''))
    except BaseCustomError as e:
        handler = ErrorHandler(log_file=f'../log/test-{os.path.splitext(os.path.basename(__file__))[0]}.log')
        handler.handle_error(e)
else:
    from lib.custom_error import ValidationError