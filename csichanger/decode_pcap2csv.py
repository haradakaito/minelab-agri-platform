import os
import sys
from datetime import datetime

from lib._csichanger import InputParser, OutputFormatter, Decoder

# 定数の定義
CSV_DIR = './result'

# 異常系処理
def handle_error(message: str):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now}] {message}")
    sys.exit(1)

# CSIデータ(.pcap)をCSVファイルに変換する
def decode_pcap2csv(filename: str) -> bool:
    try:
        # 入力パラメータの解析
        inputparser = InputParser(filename=filename)
        if not inputparser.is_valid():
            handle_error(message='入力パラメータが不正です')
        params = inputparser.get_params()

        # 振幅データ処理（抽出）
        decoder  = Decoder(filepath=params['filepath'])
        amp_list, phase_list = decoder.decode()

        # CSVファイル出力
        outputformatter = OutputFormatter()
        outputformatter.to_csv(data=amp_list, save_path=os.path.join(CSV_DIR, f"{params['filename']}_amp.csv"))     # 振幅データ
        outputformatter.to_csv(data=phase_list, save_path=os.path.join(CSV_DIR, f"{params['filename']}_phase.csv")) # 位相データ
        return True
    except Exception as e:
        handle_error(message=str(e))

if __name__ == '__main__':
    # ファイル名の入力
    filename = input('変換したいファイル名を入力してください: ')
    # CSIデータの変換
    decode_pcap2csv(filename=filename)