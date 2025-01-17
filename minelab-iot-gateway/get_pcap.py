import os
from lib import BaseCustomError, ErrorHandler, ConfigLoader, Util
from _ssh_service import SSHService

if __name__ == "__main__":
    try:
        # デバイス設定を取得
        device_config = ConfigLoader(config_path=f'{Util.get_root_dir()}/config/device-config.yaml')

        # クライアントリストを取得
        # MEMO: ネストが深すぎるかもしれないので、要検討
        for client in device_config.get('client_list'):
            # SSHサービスを初期化
            ssh_service = SSHService(
                hostname=client,
                port=device_config.get('port'),
                username=device_config.get('username')
            )

            # ファイルリストを取得
            file_list = ssh_service.get_file_list(
                remote_path=f"{device_config.get('remote_path')}",
                extention='pcap'
            )
            # ファイルを取得
            for file in file_list:
                ssh_service.get_file(
                    remote_path=f"{device_config.get('remote_path')}/{file}",
                    local_path=f"{Util.get_root_dir()}/pcap/{client}/{file}"
                )
    except BaseCustomError as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/error-{os.path.splitext(os.path.basename(__file__))[0]}.log')
        handler.handle_error(e)