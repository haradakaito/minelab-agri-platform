import os
import json
import yaml

class ConfigLoader:
    """設定ファイル（JSON/YAML）を読み込むクラス"""

    def __init__(self, config_path: str) -> None:
        self._config_path = config_path
        self._format = self._detect_format()
        self._config_data = self._load_config()

    def _detect_format(self) -> str:
        """ファイル形式を判定する関数"""
        ext = os.path.splitext(self._config_path)[1].lower()
        if ext == ".json":
            return "json"
        elif ext in [".yaml", ".yml"]:
            return "yaml"
        else:
            raise ValidationError(f"サポートされていないファイル形式です: {ext}")

    def _load_config(self) -> dict:
        """設定ファイルを読み込む関数"""
        if not os.path.exists(self._config_path):
            raise ValidationError(f"設定ファイルが存在しません: {self._config_path}")

        with open(self._config_path, 'r', encoding='utf-8') as file:
            try:
                if self._format == "json":
                    return json.load(file)
                elif self._format == "yaml":
                    return yaml.safe_load(file)
            except (json.JSONDecodeError, yaml.YAMLError) as e:
                raise ValidationError(f"設定ファイルの読み込みに失敗しました: {e}") from e

    def get(self, *keys, default=None) -> dict:
        """設定データから値を取得する関数"""
        value = self._config_data
        try:
            for key in keys:
                value = value[key]
        except (KeyError, TypeError):
            return default
        return value

    def set(self, *keys, value) -> None:
        """設定データに値を設定する関数"""
        try:
            for key in keys[:-1]:
                self._config_data = self._config_data.setdefault(key, {})
            self._config_data[keys[-1]] = value
        except (KeyError, TypeError):
            raise ValidationError(f"設定データの設定に失敗しました: {keys}")

    def save(self) -> None:
        """設定データを保存する関数"""
        try:
            with open(self._config_path, 'w', encoding='utf-8') as file:
                if self._format == "json":
                    json.dump(self._config_data, file, indent=4)
                elif self._format == "yaml":
                    yaml.dump(self._config_data, file, default_flow_style=False, allow_unicode=True, indent=4)
        except Exception as e:
            raise ValidationError(f"設定データの保存に失敗しました: {e}") from e

# 使用例
if __name__ == "__main__":
    from custom_error import BaseCustomError, ValidationError, ErrorHandler

    try:
        # JSON形式の設定ファイルを読み込む
        config_loader = ConfigLoader(config_path='../config/iam-images-config.json')
        print(config_loader.get())
        # YAML形式の設定ファイルを読み込む
        config_loader = ConfigLoader(config_path='../config/device-config.yaml')
        print(config_loader.get('project_name'))
    except BaseCustomError as e:
        handler = ErrorHandler(log_file=f'../log/test-{os.path.splitext(os.path.basename(__file__))[0]}.log')
        handler.handle_error(e)