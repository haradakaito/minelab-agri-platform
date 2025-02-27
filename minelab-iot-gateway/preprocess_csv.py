import concurrent.futures
import numpy as np
from lib_gateway import PreProcessor
from lib import Util, ErrorHandler

# 各スレッドで実行する関数
def thread_func(dirname: str):
    try:
        # 振幅データの調整
        # 位相データの調整
        pass

    except Exception as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/{Util.get_exec_file_name()}.log')
        handler.handle_error(e)

if __name__ == "__main__":
    try:

        # CSVデータを取得
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(
                    thread_func,
                    dirname
                )
                for dirname in Util.get_dir_list(path=f"{Util.get_root_dir()}/csv")
            ]
            # すべてのスレッドの完了を待つ
            concurrent.futures.wait(futures)

    except Exception as e:
        # エラーハンドラを初期化
        handler = ErrorHandler(log_file=f'{Util.get_root_dir()}/log/{Util.get_exec_file_name()}.log')
        handler.handle_error(e)
