import os
import concurrent.futures
from lib import BaseCustomError, ErrorHandler, SSHError, ConfigLoader, AESCodec, Util
from lib_gateway import SSHClient

# 各スレッドで実行する処理
def thread_func(ssh_client: SSHClient, hostname: str, exec_command: str):
    try:
        sftp = ssh_client.open_sftp(chdir="/home/pi/")
        ssh_client.exec_command(command=exec_command)
        sftp.close()
        ssh_client.close()
    except BaseCustomError as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/error-{hostname}-{os.path.splitext(os.path.basename(__file__))[0]}.log')
        handler.handle_error(e)

if __name__ == "__main__":
    try:
        # 設定ファイルを読み込む
        device_config = ConfigLoader(config_path=f'{Util.get_root_dir()}/config/device-config.yaml')
        ssh_config    = ConfigLoader(config_path=f'{Util.get_root_dir()}/config/ssh-config.json')
        exec_command  = f"{device_config.get('exec_nexmon_cmd')} {Util.get_timestamp()}.pcap"

        # AESCodec を初期化
        aes_codec = AESCodec(key=Util.get_mac_address())

        # 各デバイスごとに SSH クライアントを作成
        ssh_clients = {}
        for hostname in device_config.get("client_list"):
            ssh_client = SSHClient()
            ssh_client.connect(
                hostname=str(hostname),
                port=str(device_config.get("port")),
                username=str(device_config.get("username")),
                password=str(aes_codec.decode(encrypted_data=ssh_config.get("PASSWORD")))
            )
            ssh_clients[hostname] = ssh_client

        # マルチスレッドでコマンド実行
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(thread_func, ssh_clients[hostname], hostname, exec_command)
                for hostname in ssh_clients
            ]
            # すべてのスレッドの完了を待つ
            concurrent.futures.wait(futures)

    except BaseCustomError as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/error-{os.path.splitext(os.path.basename(__file__))[0]}.log')
        handler.handle_error(e)