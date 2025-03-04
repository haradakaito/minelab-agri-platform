import paramiko

class SSHClient:
    """SSHクライアントクラス"""
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self, hostname: str, port: str, username: str, password: str) -> None:
        """SSH接続する関数"""
        try:
            self.client.connect(hostname=hostname, port=port, username=username, password=password)
            return True
        except Exception as e:
            raise e

    def open_sftp(self, chdir: str = None) -> paramiko.SFTPClient:
        """SFTP接続する関数"""
        sftp = self.client.open_sftp()
        sftp.chdir(path=chdir) # ディレクトリ移動
        return sftp

    def exec_command(self, command: str) -> str:
        """コマンドを実行する関数"""
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode("utf-8")

    def close(self) -> None:
        """SSH切断する関数"""
        self.client.close()

# 使用例
if __name__ == '__main__':
    ssh = SSHClient()
    ssh.connect(hostname="", port="", username="", password="")
    sftp = ssh.open_sftp(chdir="/home/pi")
    print(ssh.exec_command("ls"))
    sftp.close()