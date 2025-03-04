import json
from lib import AESCodec, Util, APIClient, ErrorHandler

if __name__ == "__main__":
    try:
        # 設定ファイルを読み込む
        with open(f'{Util.get_root_dir()}/config.json', 'r') as f:
            config = json.load(f)

        # AES暗号化クラスを初期化
        aes_codec = AESCodec(key=Util.get_mac_address())

        # APIクライアントを初期化
        api_client = APIClient(
            access_key = aes_codec.decrypt(encrypted_data=config["IAMUser"]["ACCESS_KEY"]),
            secret_key = aes_codec.decrypt(encrypted_data=config["IAMUser"]["SECRET_KEY"]),
            api_key    = aes_codec.decrypt(encrypted_data=config["APIGateway"]["API_KEY"]),
            region     = aes_codec.decrypt(encrypted_data=config["APIGateway"]["REGION"]),
            service    = aes_codec.decrypt(encrypted_data=config["APIGateway"]["SERVICE"]),
            base_path  = aes_codec.decrypt(encrypted_data=config["APIGateway"]["BASE_PATH"]),
            endpoint   = aes_codec.decrypt(encrypted_data=config["APIGateway"]["ENDPOINT"])
        )

    except Exception as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/{Util.get_exec_file_name()}.log')
        handler.handle_error(e)