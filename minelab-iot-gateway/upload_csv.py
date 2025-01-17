import os
from lib import BaseCustomError, ErrorHandler, ConfigLoader, Util
from _api_service import APIService

if __name__ == "__main__":
    try:
        # APIサービスを初期化（初期化されたAPIクライアントオブジェクトを取得）
        api_service = APIService()
        api_client  = api_service.get_apiclient()

        # デバイス設定を取得
        device_config = ConfigLoader(config_path=f'{Util.get_root_dir()}/config/device-config.yaml')

        # CSVデータを取得
        with open(f'{Util.get_root_dir()}/csv/sample.csv', 'rb') as f:
            csv_data = f.read()

        # APIリクエストを送信
        response_text = api_client.send_request(
            request_path='csv',
            method='POST',
            payload={
                'device_name' : Util.get_device_name(),
                'csv_data'    : Util.encode_base64(data=csv_data),
                'project_name': device_config.get('project_name'),
                'timestamp'   : Util.get_timestamp()
            },
            timeout=10
        )
    except BaseCustomError as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/error-{os.path.splitext(os.path.basename(__file__))[0]}.log')
        handler.handle_error(e)