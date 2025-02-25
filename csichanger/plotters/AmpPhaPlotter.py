import numpy as np
import matplotlib.pyplot as plt

__all__ = ['Plotter']

class Plotter():
    """振幅と位相をプロットするクラス"""
    def __init__(self, bandwidth):
        """コンストラクタ"""
        self.bandwidth = bandwidth                # 帯域幅
        nsub       = int(bandwidth*3.2)           # サブキャリア数
        self.x_amp = np.arange(-1*nsub/2, nsub/2) # サブキャリアのインデックス
        self.x_pha = np.arange(-1*nsub/2, nsub/2) # サブキャリアのインデックス
        self.fig, axs = plt.subplots(2)           # 2つのサブプロットを作成
        self.ax_amp = axs[0]                      # 振幅
        self.ax_pha = axs[1]                      # 位相
        self.fig.suptitle('Nexmon CSI Explorer')  # タイトル

        # グラフを表示
        plt.ion()
        plt.show()

    def update(self, csi):
        """CSIを受け取り，振幅と位相をプロットする"""
        # CSIをプロット
        try:
            # グラフをクリア
            self.ax_amp.clear()
            self.ax_pha.clear()
            # ラベルを設定
            self.ax_amp.set_ylabel('Amplitude')
            self.ax_pha.set_ylabel('Phase')
            self.ax_pha.set_xlabel('Subcarrier index')
            self.ax_amp.plot(self.x_amp, np.abs(csi))
            self.ax_pha.plot(self.x_pha, np.angle(csi, deg=True))
            # グラフを更新
            plt.draw()
            plt.pause(0.001)

        except ValueError as err:
            print(f'ValueError が発生しました。帯域幅 {self.bandwidth} MHz は正しいですか？\nエラー: ', err)
            exit(-1)

    def __del__(self):
        """デストラクタ"""
        pass