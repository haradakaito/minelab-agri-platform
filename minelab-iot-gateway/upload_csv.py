import json
import concurrent.futures
from lib import AESCodec, Util, APIClient, ErrorHandler

# 各スレッドで実行する処理
def thread_func(api_client: APIClient, project_name: str, dirname: str):
    try:
        for data_type in ["amp", "pha"]:
            for file_name in Util.get_file_name_list(path=f"{Util.get_root_dir()}/csv/{dirname}/{data_type}", ext=".csv"):
                # csvファイルの読み込み
                with open(f"{Util.get_root_dir()}/csv/{dirname}/{data_type}/{file_name}", "rb") as file:
                    csv_data = file.read()

                # APIリクエストを送信
                _ = api_client.send_request(
                    request_path = 'csv', method = 'POST', timeout = 10,
                    payload = {
                        'device_name' : f"{str(dirname)}/{data_type}",
                        'csv_data'    : Util.encode_base64(data=csv_data),
                        'project_name': str(project_name),
                        'timestamp'   : Util.remove_extention(file_name=file_name)
                    }
                )

    except Exception as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/{Util.get_exec_file_name()}-{dirname}.log')
        handler.handle_error(e)

if __name__ == "__main__":
    try:
        # 設定ファイルを読み込む
        with open(f"{Util.get_root_dir()}/config/config.json", "r", encoding="utf-8") as file:
            config = json.load(file)

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

        # CSVデータを取得
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(
                    thread_func,
                    api_client,
                    aes_codec.decrypt(encrypted_data=config["ProjectName"]),
                    dirname
                )
                for dirname in Util.get_dir_list(path=f"{Util.get_root_dir()}/csv")
            ]
            # すべてのスレッドの完了を待つ
            concurrent.futures.wait(futures)

    except Exception as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/{Util.get_exec_file_name()}.log')
        handler.handle_error(e)