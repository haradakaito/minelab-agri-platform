__all__ = [
    'read_pcap'
]

import os
import numpy as np
from typing import Tuple

# 定数の定義
## サブキャリアのインデックス
NULL_SUBCARRIERS = {
    20: [x + 32 for x in [-32, -31, -30, -29, 31, 30, 29, 0]],
    40: [x + 64 for x in [-64, -63, -62, -61, -60, -59, -1, 63, 62, 61, 60, 59, 1, 0]],
    80: [x + 128 for x in [-128, -127, -126, -125, -124, -123, -1, 127, 126, 125, 124, 123, 1, 0]],
    160: [x + 256 for x in [-256, -255, -254, -253, -252, -251, -129, -128, -127, -5, -4, -3, -2, -1,
                            255, 254, 253, 252, 251, 129, 128, 127, 5, 4, 3, 3, 1, 0]]
}
## パイロットサブキャリアのインデックス
PILOT_SUBCARRIERS = {
    20: [x + 32 for x in [-21, -7, 21, 7]],
    40: [x + 64 for x in [-53, -25, -11, 53, 25, 11]],
    80: [x + 128 for x in [-103, -75, -39, -11, 103, 75, 39, 11]],
    160: [x + 256 for x in [-231, -203, -167, -139, -117, -89, -53, -25, 231, 203, 167, 139, 117, 89, 53, 25]]
}
## CSIデータのフォーマット
PCAP_HEADER_SIZE     = 24
FRAME_HEADER_SIZE    = 60
NULL_HEADER_SIZE     = 128
BYTES_PER_SUBCARRIER = 4

class SampleSet:
    """ pcapファイルから読み込んだCSIデータのサンプルセットを表すクラス """

    def __init__(self, samples: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray], bandwidth: int) -> None:
        self.rssi       = samples[0] # RSSI
        self.fctl       = samples[1] # フレーム制御情報
        self.mac        = samples[2] # MACアドレス
        self.seq        = samples[3] # シーケンス番号
        self.css        = samples[4] # コアと空間ストリーム情報
        self.csi        = samples[5] # CSIデータ
        self.nsamples   = self.csi.shape[0] # サンプル数
        self.bandwidth  = bandwidth # 帯域幅

    def get_rssi(self, index: int) -> int:
        """ 指定インデックスのRSSI取得 """
        return self.rssi[index]

    def get_fctl(self, index: int) -> int:
        """ 指定インデックスのフレーム制御情報取得 """
        return self.fctl[index]

    def get_mac(self, index: int) -> bytes:
        """ 指定インデックスのMACアドレス取得 """
        return self.mac[index*6 : (index+1)*6]

    def get_seq(self, index: int) -> Tuple[int, int]:
        """ 指定インデックスのシーケンス番号取得 """
        sc = int.from_bytes(self.seq[index*2 : (index+1)*2], byteorder='little', signed=False)
        fn = sc%16
        sc = int((sc-fn)/16)
        return (sc, fn)

    def get_css(self, index: int) -> bytes:
        """ 指定インデックスのコアと空間ストリーム情報取得 """
        return self.css[index*2 : (index+1)*2]

    def get_csi(self, index: int, rm_nulls: bool = False, rm_pilots: bool = False) -> np.ndarray:
        """ 指定インデックスのCSIデータ取得 """
        csi = self.csi[index].copy()
        if rm_nulls:
            csi[NULL_SUBCARRIERS[self.bandwidth]] = 0
        if rm_pilots:
            csi[PILOT_SUBCARRIERS[self.bandwidth]] = 0
        return csi

    def print(self, index: int) -> None:
        """ 指定インデックスに対応するサンプル情報出力 """
        macid = self.get_mac(index).hex()
        macid = ':'.join([macid[i:i+2] for i in range(0, len(macid), 2)])
        sc, fn = self.get_seq(index)
        css    = self.get_css(index).hex()
        rssi   = self.get_rssi(index)
        fctl   = self.get_fctl(index)

def __find_bandwidth(incl_len: bytes) -> int:
    """ 帯域幅の検出 """
    pkt_len   = int.from_bytes(incl_len, byteorder='little', signed=False)
    pkt_len  += (NULL_HEADER_SIZE-FRAME_HEADER_SIZE)
    bandwidth = 20 * int(pkt_len//(20*3.2*BYTES_PER_SUBCARRIER))
    return bandwidth

def __find_nsamples_max(pcap_filesize: int, nsub: int) -> int:
    """ サンプル数の最大値計算 """
    return int((pcap_filesize-PCAP_HEADER_SIZE) / (12+46+18+(nsub*BYTES_PER_SUBCARRIER)))

def read_pcap(pcap_filepath: str, bandwidth: int = 0, nsamples_max: int = 0) -> SampleSet:
    """ pcapファイルの読み込みとCSIデータのSampleSet生成 """
    pcap_filesize = os.stat(pcap_filepath).st_size
    with open(pcap_filepath, 'rb') as pcapfile:
        fc = pcapfile.read()

    if bandwidth == 0:
        bandwidth = __find_bandwidth(fc[32:36])
    nsub = int(bandwidth * 3.2)

    if nsamples_max == 0:
        nsamples_max = __find_nsamples_max(pcap_filesize, nsub)

    rssi = bytearray(nsamples_max*1)
    fctl = bytearray(nsamples_max*1)
    mac  = bytearray(nsamples_max*6)
    seq  = bytearray(nsamples_max*2)
    css  = bytearray(nsamples_max*2)
    csi  = bytearray(nsamples_max*nsub*BYTES_PER_SUBCARRIER)
    ptr  = PCAP_HEADER_SIZE

    nsamples = 0
    while ptr < pcap_filesize:
        ptr += 8
        frame_len = int.from_bytes(fc[ptr : ptr+4], byteorder='little', signed=False)
        ptr += 50

        rssi[nsamples] = fc[ptr+2]
        fctl[nsamples] = fc[ptr+3]
        mac[nsamples*6 : (nsamples+1)*6] = fc[ptr+4 : ptr+10]
        seq[nsamples*2 : (nsamples+1)*2] = fc[ptr+10 : ptr+12]
        css[nsamples*2 : (nsamples+1)*2] = fc[ptr+12 : ptr+14]
        csi[nsamples*(nsub*BYTES_PER_SUBCARRIER) : (nsamples+1)*(nsub*BYTES_PER_SUBCARRIER)] = fc[ptr+18 : ptr+18+nsub*BYTES_PER_SUBCARRIER]

        ptr += (frame_len-42)
        nsamples += 1

    csi_np    = np.frombuffer(csi, dtype=np.int16, count=nsub*2*nsamples).reshape((nsamples, nsub*2))
    csi_cmplx = np.fft.fftshift(csi_np[:nsamples, ::2] + 1.j * csi_np[:nsamples, 1::2], axes=(1,))
    rssi      = np.frombuffer(rssi, dtype=np.int8, count=nsamples)

    return SampleSet((rssi, fctl, mac, seq, css, csi_cmplx), bandwidth)