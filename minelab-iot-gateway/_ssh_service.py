from lib import BaseCustomError, Util, ConfigLoader, AESCodec
from lib_gateway import SSHClient

from fnmatch import fnmatch

class SSHService:
    def __init__(self, hostname: str, port: str, username: str):
        """SSHサービスを初期化する"""
        try:
            # SSHクライアントを初期化
            self.ssh_client = SSHClient()
        except BaseCustomError as e:
            raise e

        # 暗号化・復号化クラスを初期化（暗号化キーを指定）
        try:
            codec = AESCodec(key=Util.get_mac_address())
        except BaseCustomError as e:
            raise e

        # 設定ファイルを読み込む
        try:
            ssh_config = ConfigLoader(config_path=f'{Util.get_root_dir()}/config/ssh-config.json')
            self.hostname   = hostname
            self.port       = port
            self.username   = username
            self.password   = codec.decode(encrypted_data=ssh_config.get('PASSWORD'))
        except BaseCustomError as e:
            raise e

    def get_file_list(self, remote_path: str, chdir: str = None, extention: str = None) -> list:
        """リモートのファイルリストを取得する関数"""
        try:
            # ファイルリストを取得する
            self.ssh_client.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)
            sftp = self.ssh_client.open_sftp(chdir=remote_path)
            if extention is not None:
                file_list = [file for file in sftp.listdir() if fnmatch(file, f"*.{extention}")]
            else:
                file_list = sftp.listdir()
            sftp.close()
            return file_list
        except BaseCustomError as e:
            raise e
        finally:
            self.ssh_client.close()

    def get_file(self, remote_path: str, local_path: str, chdir: str = None) -> None:
        """リモートファイルをダウンロードする関数"""
        try:
            # ディレクトリが存在しない場合は作成する
            Util.create_path(path=local_path)
            # ファイルをダウンロードする
            self.ssh_client.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)
            sftp = self.ssh_client.open_sftp(chdir=chdir)
            sftp.get(remotepath=remote_path, localpath=local_path)
            sftp.close()
        except BaseCustomError as e:
            raise e
        finally:
            self.ssh_client.close()