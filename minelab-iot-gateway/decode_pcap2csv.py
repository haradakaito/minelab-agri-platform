import time
import importlib
import config
from lib_gateway.AmpPhaPlotter import Plotter
decoder = importlib.import_module(f'lib_gateway.{config.decoder}')

def string_is_int(s):
    """文字列が整数であるかをチェックする関数"""
    try:
        int(s)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    pcap_filename = input('Pcapファイル名: ')

    if '.pcap' not in pcap_filename:
        pcap_filename += '.pcap'
    pcap_filepath = '/'.join([config.pcap_fileroot, pcap_filename])

    try:
        # パケットデータを読み込む
        samples = decoder.read_pcap(pcap_filepath)
        # プロッターを初期化
        if config.plot_samples:
            plotter = Plotter(samples.bandwidth)
        # パケットデータをプロットする
        while True:
            # コマンドを受け取る
            command = input('> ')
            # コマンドに応じて処理を行う
            ## ヘルプメッセージを表示
            if 'help' in command:
                print(config.help_str)
            ## プログラムを終了
            elif 'exit' in command:
                break
            ## # ハイフンが含まれている場合、範囲指定として処理
            elif ('-' in command) and string_is_int(command.split('-')[0]) and string_is_int(command.split('-')[1]):
                # ハイフンで分割して範囲を取得
                start = int(command.split('-')[0])
                end   = int(command.split('-')[1])
                # サンプルの範囲をプロット
                for index in range(start, end+1):
                    # CSIサンプルをプロンプトに表示
                    if config.print_samples:
                        samples.print(index)
                    # CSIをプロット
                    if config.plot_samples:
                        csi = samples.get_csi(index, config.remove_null_subcarriers, config.remove_pilot_subcarriers)
                        plotter.update(csi)
                    # アニメーションを遅延
                    time.sleep(config.plot_animation_delay_s)
            ## コマンドが整数の場合、そのインデックスのCSIをプロット
            elif string_is_int(command):
                # インデックスを取得
                index = int(command)
                # CSIサンプルをプロンプトに表示
                if config.print_samples:
                    samples.print(index)
                # CSIをプロット
                if config.plot_samples:
                        csi = samples.get_csi(index, config.remove_null_subcarriers, config.remove_pilot_subcarriers)
                        plotter.update(csi)
            ## それ以外の場合、不明なコマンドとして処理
            else:
                print('Unknown command. Type help.')

    except Exception as e:
        print(e)