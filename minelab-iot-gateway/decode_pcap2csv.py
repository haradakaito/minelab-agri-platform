import importlib
import config
decoder = importlib.import_module(f'lib_gateway.{config.decoder}')

if __name__ == "__main__":
    try:
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