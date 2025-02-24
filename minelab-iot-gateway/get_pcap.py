import json
from fnmatch import fnmatch
from lib import AESCodec, Util, ErrorHandler
from lib_gateway import SSHClient

if __name__ == "__main__":
    try:
        # 設定ファイルを読み込む
        with open(f"{Util.get_root_dir()}/config/config.json", "r", encoding="utf-8") as file:
            config = json.load(file)

        # AES暗号化クラスを初期化
        aes_codec = AESCodec(key=Util.get_mac_address())

        # 各クライアントのpcapファイルを取得
        for hostname in config["SSHConnect"]["HOSTNAME_LIST"]:
            # SSHクライアントを初期化
            ssh_client = SSHClient()
            # SSH接続を確立
            ssh_client.connect(
                hostname = aes_codec.decrypt(encrypted_data=hostname),
                port     = aes_codec.decrypt(encrypted_data=config["SSHConnect"]["PORT"]),
                username = aes_codec.decrypt(encrypted_data=config["SSHConnect"]["USERNAME"]),
                password = aes_codec.decrypt(encrypted_data=config["SSHConnect"]["PASSWORD"])
            )

            # Pcapファイルリストを取得
            sftp = ssh_client.open_sftp(
                chdir = aes_codec.decrypt(encrypted_data=config["SSHConnect"]["REMOTE_PATH"])
            )
            file_list = [file for file in sftp.listdir() if fnmatch(file, f"*.pcap")]

            # Pcapファイルを取得
            # 保存先のパス確認
            Util.create_path(path=f"{aes_codec.decrypt(encrypted_data=config['SSHConnect']['LOCAL_PATH'])}/{aes_codec.decrypt(encrypted_data=hostname)}/")
            for file in file_list:
                sftp.get(
                    remotepath = f"{aes_codec.decrypt(encrypted_data=config['SSHConnect']['REMOTE_PATH'])}/{file}",
                    localpath  = f"{aes_codec.decrypt(encrypted_data=config['SSHConnect']['LOCAL_PATH'])}/{aes_codec.decrypt(encrypted_data=hostname)}/{file}/"
                )

            # SSH接続を切断
            sftp.close()
            ssh_client.close()

    except Exception as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/{Util.get_exec_file_name()}.log')
        handler.handle_error(e)