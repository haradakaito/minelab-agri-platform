import json
from lib import AESCodec, Util, APIClient, ErrorHandler
from lib_camera import Camera

if __name__ == "__main__":
    try:
        # カメラを初期化して撮影・保存
        camera = Camera()
        camera.capture()
        camera.save()

        # 設定ファイルを読み込む
        with open(f"{Util.get_root_dir()}/config/config.json", "r", encoding="utf-8") as file:
            config = json.load(file)

        # APIクライアントを初期化
        api_client = APIClient(
            access_key = AESCodec(key=Util.get_mac_address()).decrypt(encrypted_data=config["IAMUser"]["ACCESS_KEY"]),
            secret_key = AESCodec(key=Util.get_mac_address()).decrypt(encrypted_data=config["IAMUser"]["SECRET_KEY"]),
            api_key    = AESCodec(key=Util.get_mac_address()).decrypt(encrypted_data=config["APIGateway"]["API_KEY"]),
            region     = AESCodec(key=Util.get_mac_address()).decrypt(encrypted_data=config["APIGateway"]["REGION"]),
            service    = AESCodec(key=Util.get_mac_address()).decrypt(encrypted_data=config["APIGateway"]["SERVICE"]),
            base_path  = AESCodec(key=Util.get_mac_address()).decrypt(encrypted_data=config["APIGateway"]["BASE_PATH"]),
            endpoint   = AESCodec(key=Util.get_mac_address()).decrypt(encrypted_data=config["APIGateway"]["ENDPOINT"])
        )

        # APIリクエストを送信
        response_text = api_client.send_request(
            request_path='images',
            method='POST',
            payload={
                'device_name' : Util.get_device_name(),
                'image_data'  : Util.encode_base64(data=camera.get()),
                'project_name': AESCodec(key=Util.get_mac_address()).decrypt(encrypted_data=config["ProjectName"]),
                'timestamp'   : Util.get_timestamp()
            },
            timeout=10
        )

    except Exception as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/{Util.get_exec_file_name()}.log')
        handler.handle_error(e)
    finally:
        camera.clear()