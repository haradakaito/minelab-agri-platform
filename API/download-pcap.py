import json
import os
import base64
import boto3

# 定数
BUCKET_NAME = os.environ['BUCKET_NAME']

# クエリパラメータのバリデーション
def _is_valid_params(params: dict) -> bool:
    try:
        # 必須キーの存在確認
        required_keys = ['device_name', 'project_name', 'year', 'month', 'day']
        if not all(key in params for key in required_keys):
            return False

        # 型チェック
        return all(isinstance(params[key], str) for key in required_keys)

    except (KeyError, TypeError):
        return False  # キーが存在しない、または型が不正な場合は False

def lambda_handler(event, context):
    try:
        # クエリパラメータの検証
        if not _is_valid_params(event.get("queryStringParameters", {})):
            return {
                'statusCode': 400,
                'body': json.dumps('The payload is invalid.')
            }

        # S3 クライアント
        s3 = boto3.client('s3')

        # クエリパラメータの取得
        params = event["queryStringParameters"]
        device_name  = params['device_name']
        project_name = params['project_name']
        year         = params['year']
        month        = params['month']
        day          = params['day']

        # 取得対象のプレフィックス（S3の仮想フォルダ）
        prefix = f'projects/{project_name}/pcap-data/{device_name}/year={year}/month={month}/day={day}/'

        # S3の対象フォルダ内の全オブジェクトをリストアップ
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)

        # ファイルが存在しない場合
        if 'Contents' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps('No pcaps found.')
            }

        # pcapデータを取得
        pcaps = []
        for obj in response['Contents']:
            key = obj['Key']
            if key.endswith('.pcap'):  # pcapのみ取得
                file_obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
                file_content = file_obj['Body'].read()
                pcaps.append({
                    "file_name": os.path.basename(key),
                    "pcap_data": base64.b64encode(file_content).decode('utf-8')  # Base64エンコード
                })

        return {
            'statusCode': 200,
            'body': json.dumps(pcaps)  # pcapリストを返す
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }