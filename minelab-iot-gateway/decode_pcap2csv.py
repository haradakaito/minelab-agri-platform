import json
import importlib
import config
from lib import Util, AESCodec

if __name__ == "__main__":
    try:
        # 設定ファイルの読み込み
        with open(f"{Util.get_root_dir()}/config/config.json", "r", encoding="utf-8") as file:
            _config = json.load(file)

        # AES暗号化クラスを初期化
        aes_codec = AESCodec(key=Util.get_mac_address())

        # デコーダを読み込み
        decoder = importlib.import_module(f"lib_gateway.{aes_codec.decrypt(encrypted_data=_config['CSIChanger']['DECODER'])}")

        # Pcapファイル名を入力
        pcap_filename = input('Pcapファイル名: ')
        # 拡張子がない場合は付与する
        if '.pcap' not in pcap_filename:
            pcap_filename += '.pcap'
        pcap_filepath = '/'.join([config.pcap_fileroot, pcap_filename])
        # パケットデータを読み込む
        samples = decoder.read_pcap(pcap_filepath)
    except Exception as e:
        print(e)