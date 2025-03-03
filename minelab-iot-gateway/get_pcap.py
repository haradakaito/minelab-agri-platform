import json
import concurrent.futures
from fnmatch import fnmatch
from lib import AESCodec, Util, ErrorHandler
from lib_gateway import SSHClient

# 各スレッドで実行する処理
def thread_func(ssh_client: SSHClient, remote_path: str, local_path: str):
    """各ホストに対してPcapファイルを取得する処理"""
    try:
        # 保存先のパス確認
        Util.create_path(path=local_path)
        # Pcapファイルリストを取得
        sftp = ssh_client.open_sftp(chdir=remote_path)
        file_list = [file for file in sftp.listdir() if fnmatch(file, f"*.pcap")]
        # Pcapファイルを取得
        for file in file_list:
            sftp.get(remotepath=f"{remote_path}/{file}", localpath=f"{local_path}/{file}")

        # SSH接続を切断
        sftp.close()
        ssh_client.close()

    except Exception as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/{Util.get_exec_file_name()}.log')
        handler.handle_error(e)

if __name__ == "__main__":
    try:
        # 設定ファイルを読み込む
        with open(f"{Util.get_root_dir()}/config/config.json", "r", encoding="utf-8") as file:
            config = json.load(file)

        # AES暗号化クラスを初期化
        aes_codec = AESCodec(key=Util.get_mac_address())

        # 各クライアントのpcapファイルを取得
        ssh_clients = {}
        for hostname in config["SSHConnect"]["HOSTNAME_LIST"]:
            # SSHクライアントを初期化
            ssh_client = SSHClient()
            # SSH接続を確立
            ssh_client.connect(
                hostname = f"{aes_codec.decrypt(encrypted_data=hostname)}.local",
                port     = aes_codec.decrypt(encrypted_data=config["SSHConnect"]["PORT"]),
                username = aes_codec.decrypt(encrypted_data=config["SSHConnect"]["USERNAME"]),
                password = aes_codec.decrypt(encrypted_data=config["SSHConnect"]["PASSWORD"])
            )
            ssh_clients[aes_codec.decrypt(encrypted_data=hostname)] = ssh_client

        # マルチスレッドでコマンド実行
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(
                    thread_func,
                    ssh_clients[aes_codec.decrypt(encrypted_data=hostname)],                   # SSHクライアント
                    aes_codec.decrypt(encrypted_data=config["SSHConnect"]["REMOTE_PATH"]),     # リモートパス（取得先）
                    f"{Util.get_root_dir()}/pcap/{aes_codec.decrypt(encrypted_data=hostname)}" # ローカルパス（保存先）
                )
                for hostname in config["SSHConnect"]["HOSTNAME_LIST"]
            ]
            # すべてのスレッドの完了を待つ
            concurrent.futures.wait(futures)

    except Exception as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/{Util.get_exec_file_name()}.log')
        handler.handle_error(e)