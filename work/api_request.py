import os
from lib import BaseCustomError, ErrorHandler, Util
from api_service import APIService

if __name__ == "__main__":
    try:
        # APIサービスを初期化（初期化されたAPIクライアントオブジェクトを取得）
        api_service = APIService()
        api_client  = api_service.get_apiclient()

        # APIリクエストを送信
        response_text = api_client.send_request(
            request_path='images',
            method='GET',
            timeout=10
        )
        print(response_text)
    except BaseCustomError as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/{os.path.splitext(os.path.basename(__file__))[0]}.log')
        handler.handle_error(e)