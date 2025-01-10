from lib import APIClient, ConfigLoader, AESCodec, Util, BaseCustomError, ErrorHandler

class APIService:
    def __init__(self):
        """APIサービスを初期化する"""
        try:
            # 設定ファイルを読み込む
            api_config = ConfigLoader(config_path=f'{Util.get_root_dir()}/config/api-config.json') # API設定ファイル
            iam_config = ConfigLoader(config_path=f'{Util.get_root_dir()}/config/iam-config.json') # IAM設定ファイル
        except BaseCustomError as e:
            raise e

        # 暗号化・復号化クラスを初期化（暗号化キーを指定）
        try:
            codec = AESCodec(key=Util.get_mac_address())
        except BaseCustomError as e:
            raise e

        # APIクライアントを初期化
        try:
            self.api_client = APIClient(
                access_key   = codec.decode(encrypted_data=iam_config.get('AWS_ACCESS_KEY')),
                secret_key   = codec.decode(encrypted_data=iam_config.get('AWS_SECRET_KEY')),
                api_key      = codec.decode(encrypted_data=iam_config.get('API_KEY')),
                region       = api_config.get('REGION'),
                service      = api_config.get('SERVICE'),
                base_path    = api_config.get('BASE_PATH'),
                api_endpoint = f"{api_config.get('API_ID')}.{api_config.get('SERVICE')}.{api_config.get('REGION')}.{api_config.get('HOST')}"
            )
        except BaseCustomError as e:
            raise e

    def get_apiclient(self):
        return self.api_client