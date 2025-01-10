import os
from lib import BaseCustomError, ErrorHandler, Util, Camera
from api_service import APIService

# 定数
PROJECT_NAME = 'csi' # プロジェクト名

if __name__ == "__main__":
    try:
        # カメラを初期化
        camera = Camera()

        # APIサービスを初期化（初期化されたAPIクライアントオブジェクトを取得）
        api_service = APIService()
        api_client  = api_service.get_apiclient()

        # APIリクエストを送信
        response_text = api_client.send_request(
            request_path='images',
            method='POST',
            payload={
                'device_name' : Util.get_device_name(),
                'image_data'  : Util.encode_base64(camera.encode_frame(frame=camera.capture(), ext='.jpg')),
                'project_name': PROJECT_NAME,
                'timestamp'   : Util.get_timestamp()
            },
            timeout=3
        )
    except BaseCustomError as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/{os.path.splitext(__file__)[0]}.log')
        handler.handle_error(e)