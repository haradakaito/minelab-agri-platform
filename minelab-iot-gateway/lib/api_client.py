import requests
import json
from botocore.awsrequest import AWSRequest
from botocore.auth import SigV4Auth
from botocore.credentials import Credentials

class APIClient:
    """APIクライアントクラス（AWS SigV4署名を用いてAPIリクエストを送信する）"""
    def __init__(self, access_key: str, secret_key: str, api_key: str, region: str, service: str, base_path: str, endpoint: str) -> None:
        """APIクライアントの初期化"""
        self.credentials  = Credentials(access_key, secret_key) # AWS認証情報
        self.region       = region    # リージョン
        self.service      = service   # サービス名
        self.api_key      = api_key   # APIキー
        self.endpoint     = endpoint  # APIエンドポイント
        self.api_basepath = base_path # APIベースパス

    def _create_signed_request(self, method: str, url: str, payload: str=None) -> AWSRequest:
        """AWS SigV4署名付きリクエストを生成する"""
        try:
            request = AWSRequest(method=method, url=url, data=payload)
            SigV4Auth(self.credentials, self.service, self.region).add_auth(request)
            return request
        except Exception as e:
            raise e

    def _get_headers(self, request: AWSRequest) -> dict:
        """リクエストヘッダーを取得する"""
        return {
            'Authorization': request.headers['Authorization'],
            'Host'         : self.endpoint,
            'X-Amz-Date'   : request.headers['X-Amz-Date'],
            'X-Api-Key'    : self.api_key,
            'Content-Type' : 'application/json'
        }

    def send_request(self, request_path: str, method: str, params: dict=None, payload: dict=None, timeout: int=10) -> str:
        """
        APIリクエストを送信する

        Parameters
        ----------
        request_path : str
            リクエストパス
        method : str
            HTTPメソッド（GET, POST, PUT, DELETE）
        payload : str, default None
            リクエストボディ
        timeout : int, default 10
            タイムアウト時間（秒）

        Returns
        -------
        response_text : str
            レスポンステキスト

        Raises
        ------
        APIError
            APIリクエストの送信に失敗した場合に発生する例外

        Notes
        -----
        - リクエストURLは、APIエンドポイントとリクエストパスから生成される
        - リクエストヘッダーは、署名付きリクエストから取得する
        """
        try:
            url = f"https://{self.endpoint}/{self.api_basepath}/{request_path}"                        # リクエストURLを生成
            request = self._create_signed_request(method=method, url=url, payload=json.dumps(payload)) # 署名付きリクエストを生成
            headers = self._get_headers(request=request)                                               # ヘッダーを設定

            # リクエストを送信
            if method == "POST":
                response = requests.request(method=method, url=url, headers=headers, data=json.dumps(payload), timeout=timeout)
            else:
                response = requests.request(method=method, url=url, headers=headers, params=json.dumps(params), data=json.dumps(payload), timeout=timeout)
            response.raise_for_status() # ステータスコードが200番台以外の場合は例外を発生させる
            return response
        except Exception as e:
            raise e