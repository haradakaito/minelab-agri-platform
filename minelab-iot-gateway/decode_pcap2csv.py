import json
import concurrent.futures
import importlib
import numpy as np
import pandas as pd

from lib import Util, AESCodec, ErrorHandler

# 各スレッドで実行する処理
def thread_func(hostname: str, pcap_path: str, csv_path: str):
    """PcapデータをCSVに変換する"""
    try:
        # 保存先のパス確認（存在しない場合は作成）
        Util.create_path(path=f"{csv_path}/amp/")
        Util.create_path(path=f"{csv_path}/pha/")
        # 各ファイルの変換処理
        for filename in Util.get_file_name_list(path=f"{pcap_path}/{hostname}", ext=".pcap"):
            # Pcapファイルの読み込み
            samples = decoder.read_pcap(pcap_filepath=f"{pcap_path}/{hostname}/{filename}")
            # 振幅データの抽出
            csi_amp_df = pd.DataFrame(
                [np.abs(samples.get_csi(index=index, rm_nulls=True, rm_pilots=False)) for index in range(samples.nsamples)]
            )
            # 位相データの抽出
            csi_pha_df = pd.DataFrame(
                [np.angle(samples.get_csi(index=index, rm_nulls=True, rm_pilots=False)) for index in range(samples.nsamples)]
            )
            # データをcsvで保存
            csi_amp_df.to_csv(f"{csv_path}/amp/{Util.remove_extention(file_name=filename)}.csv")
            csi_pha_df.to_csv(f"{csv_path}/pha/{Util.remove_extention(file_name=filename)}.csv")

    except Exception as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/{Util.get_exec_file_name()}.log')
        handler.handle_error(e)

if __name__ == "__main__":
    try:
        # 設定ファイルの読み込み
        with open(f"{Util.get_root_dir()}/config/config.json", "r", encoding="utf-8") as file:
            config = json.load(file)

        # AES暗号化クラスを初期化
        aes_codec = AESCodec(key=Util.get_mac_address())

        # デコーダの読み込み
        decoder = importlib.import_module(f"lib_gateway.{aes_codec.decrypt(encrypted_data=config['CSIChanger']['DECODER'])}")

        # pcapデータをcsvに変換
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(
                    thread_func,
                    aes_codec.decrypt(encrypted_data=hostname),                                # ホスト名
                    f"{Util.get_root_dir()}/pcap/{aes_codec.decrypt(encrypted_data=hostname)}" # pcapファイルの取得先
                    f"{Util.get_root_dir()}/csv/{aes_codec.decrypt(encrypted_data=hostname)}"  # csvファイルの保存先
                )
                for hostname in config["SSHConnect"]["HOSTNAME_LIST"]
            ]
            # スレッドの終了を待つ
            concurrent.futures.wait(futures)

    except Exception as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/{Util.get_exec_file_name()}.log')
        handler.handle_error(e)