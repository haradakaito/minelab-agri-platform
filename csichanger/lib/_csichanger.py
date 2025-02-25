import os
import importlib

import numpy as np
import pandas as pd

from config import config

# 定数の定義
DECODER_DIR = 'lib'

class Decoder:
    def __init__(self, filepath) -> None:
        self.decoder  = importlib.import_module(f'{DECODER_DIR}.{config.decoder}')
        self.filepath = filepath

    def decode(self) -> object:
        samples = self.decoder.read_pcap(self.filepath)
        # RSSIデータ処理
        amp_list = [
            np.abs(
                samples.get_csi(
                    index,
                    config.remove_null_subcarriers,
                    config.remove_pilot_subcarriers
                )
            )
            for index in range(samples.nsamples)
        ]
        # 位相データ処理
        phase_list = [
            np.angle(
                samples.get_csi(
                    index,
                    config.remove_null_subcarriers,
                    config.remove_pilot_subcarriers
                )
            )
            for index in range(samples.nsamples)
        ]
        return amp_list, phase_list

class InputParser:
    def __init__(self, filename: str) -> None:
        self.filename  = filename

    def get_params(self) -> dict:
        filename    = self.filename
        filepath    = os.path.join(config.pcap_fileroot, f'{filename}.pcap')
        return {
            'filename': filename,
            'filepath': filepath
        }

    def is_valid(self) -> bool:
        return all([
            self._is_filename_valid(),
            self._is_file_exists()
        ])

    def _is_filename_valid(self) -> bool:
        return '.pcap' not in self.filename

    def _is_file_exists(self) -> bool:
        fileroot = config.pcap_fileroot
        return os.path.exists(os.path.join(fileroot, f'{self.filename}.pcap'))

class OutputFormatter:
    def to_csv(self, data: list, save_path: str) -> None:
        df = pd.DataFrame(data)
        df.to_csv(save_path)