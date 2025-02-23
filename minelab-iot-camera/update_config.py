import json
from lib import AESCodec, Util, ErrorHandler

def process_json_values(data, func):
    """JSONデータ内の全てのデータに対して任意の関数（func）を適用する関数"""
    if isinstance(data, dict):
        return {key: process_json_values(value, func) for key, value in data.items()}
    elif isinstance(data, list):
        return [process_json_values(item, func) for item in data]
    else:
        return func(data)

if __name__ == "__main__":
    try:
        # 設定ファイルを読み込む
        with open(f"{Util.get_root_dir()}/config/config.json", "r", encoding="utf-8") as file:
            encrypt_config = json.load(file)
        # 設定ファイルを復号化
        decrypt_config = process_json_values(data=encrypt_config, func=lambda x: AESCodec(key=Util.get_mac_address()).decrypt(encrypted_data=x))
        # 設定ファイルを暗号化
        encrypt_config = process_json_values(data=decrypt_config, func=lambda x: AESCodec(key=Util.get_mac_address()).encrypt(plaintext=x))
        # 設定ファイルを保存
        with open(f"{Util.get_root_dir()}/config/config.json", "w", encoding="utf-8") as file:
            json.dump(encrypt_config, file, indent=4, ensure_ascii=False)

    except Exception as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/{Util.get_exec_file_name()}.log')
        handler.handle_error(e)