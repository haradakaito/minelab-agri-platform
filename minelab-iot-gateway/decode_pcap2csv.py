import json
import importlib
import numpy as np
import pandas as pd

from lib import Util, AESCodec, ErrorHandler

if __name__ == "__main__":
    try:
        # 設定ファイルの読み込み
        with open(f"{Util.get_root_dir()}/config/config.json", "r", encoding="utf-8") as file:
            config = json.load(file)

        # AES暗号化クラスを初期化
        aes_codec = AESCodec(key=Util.get_mac_address())

        # デコーダの読み込み
        decoder = importlib.import_module(f"lib_gateway.{aes_codec.decrypt(encrypted_data=config['CSIChanger']['DECODER'])}")

        # pcapファイル名リストを取得
        root_path = Util.get_root_dir()
        for dirname in Util.get_dir_list(path=f"{root_path}/pcap"):
            for filename in Util.get_file_name_list(path=f"{root_path}/pcap/{dirname}", ext=".pcap"):
                # Pcapファイルの読み込み
                samples = decoder.read_pcap(pcap_filepath=f"{root_path}/pcap/{dirname}/{filename}")
                # データの抽出
                csi_amp = [np.abs(samples.get_csi(index=index, rm_nulls=True, rm_pilots=False)) for index in range(2)]   # 振幅
                csi_pha = [np.angle(samples.get_csi(index=index, rm_nulls=True, rm_pilots=False)) for index in range(2)] # 位相
                # データをcsvで保存
                df_amp = pd.DataFrame(csi_amp)
                df_pha = pd.DataFrame(csi_pha)
                df_amp.to_csv(f"{Util.get_root_dir()}/csv/{dirname}/amp/{Util.remove_extention(file_name=filename)}.csv")
                df_pha.to_csv(f"{Util.get_root_dir()}/csv/{dirname}/pha/{Util.remove_extention(file_name=filename)}.csv")

    except Exception as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/{Util.get_exec_file_name()}.log')
        handler.handle_error(e)