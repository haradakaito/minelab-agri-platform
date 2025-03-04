import json
import os
import base64
import boto3

# 定数
BUCKET_NAME = os.environ['BUCKET_NAME']

# ペイロードのバリデーション
def _is_valid_payload(payload: dict) -> bool:
    try:
        # 必須キーの存在確認
        required_keys = ['device_name', 'pcap_data', 'project_name', 'timestamp']
        if not all(key in payload for key in required_keys):
            return False

        # 型チェック
        return (
            isinstance(payload['device_name'], str) and
            isinstance(payload['pcap_data'], str) and
            isinstance(payload['project_name'], str) and
            isinstance(payload['timestamp'], str)
        )
    except (KeyError, TypeError):
        return False  # キーが存在しない、または型が不正な場合は False

# 保存パスの作成
def _create_save_path(project_name: str, device_name: str, timestamp: str):
    # YYYY-MM-DDThh:mm:ssの場合、year=YYYY/month=MM/day=DD/YYYMMDDhhmmss.pcap
    year      = timestamp.split('T')[0].split('-')[0]
    month     = timestamp.split('T')[0].split('-')[1]
    day       = timestamp.split('T')[0].split('-')[2]
    file_name = timestamp.split('T')[0].replace('-', '') + timestamp.split('T')[1].replace('-', '') + '.pcap'
    return f'projects/{project_name}/pcap-data/{device_name}/year={year}/month={month}/day={day}/{file_name}'

def lambda_handler(event, context):
    try:
        # ペイロードの検証
        if _is_valid_payload(payload=event):

            # PCAP保存処理
            s3 = boto3.client('s3')
            pcap_data = base64.b64decode(event['pcap_data'])
            save_path  = _create_save_path(project_name=event['project_name'], device_name=event['device_name'], timestamp=event['timestamp'])
            s3.put_object(Bucket=BUCKET_NAME, Key=save_path, Body=pcap_data)

            return {
                'statusCode': 200,
                'body': json.dumps('PCAP uploaded successfully.')
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('The payload is invalid.')
            }
    except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps(f'Error: {e}')
            }