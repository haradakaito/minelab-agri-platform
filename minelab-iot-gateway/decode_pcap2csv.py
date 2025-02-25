import json
import importlib
import numpy as np
from lib import Util, AESCodec, ErrorHandler

if __name__ == "__main__":
    try:
        # 設定ファイルの読み込み
        with open(f"{Util.get_root_dir()}/config/config.json", "r", encoding="utf-8") as file:
            config = json.load(file)

        # AES暗号化クラスを初期化
        aes_codec = AESCodec(key=Util.get_mac_address())

        # デコーダを読み込み
        decoder = importlib.import_module(f"lib_gateway.{aes_codec.decrypt(encrypted_data=config['CSIChanger']['DECODER'])}")

        # pcapファイル名リストを取得
        root_path = Util.get_root_dir()
        for dirname in Util.get_dir_list(path=f"{root_path}/pcap"):
            for filename in Util.get_file_name_list(path=f"{root_path}/pcap/{dirname}", ext=".pcap"):
                samples = decoder.read_pcap(pcap_filepath=f"{root_path}/pcap/{dirname}/{filename}")
                for index in range(2):
                    csi = samples.get_csi(index, aes_codec.decrypt(encrypted_data=config["CSIChanger"]["REMOVE_NULL_SUBCARRIERS"]), aes_codec.decrypt(encrypted_data=config["CSIChanger"]["REMOVE_PILOT_SUBCARRIERS"]))
                    print("振幅：", np.abs(csi))
                    print("位相：", np.angle(csi))

    except Exception as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/{Util.get_exec_file_name()}.log')
        handler.handle_error(e)