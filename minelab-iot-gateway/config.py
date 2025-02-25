# 使用するWi-Fiチップ（1つ以外コメントアウト）
chip = 'bcm43455c0' # Raspberry Pi 3B+ and 4B
# chip = 'bcm4339'    # Nexus 5
# chip = 'bcm4358'    # Nexus 6P
# chip = 'bcm4366c0'  # Asus RT-AC86U

# pcapファイルのルートディレクトリ
pcap_fileroot = 'pcap'

# 出力設定
print_samples = True           # ターミナルへの出力設定
plot_samples  = True           # プロットの出力設定
plot_animation_delay_s = 0.005 # プロットのアニメーションの遅延時間（秒）

# Nullサブキャリアの削除設定
remove_null_subcarriers = True

# パイロットサブキャリアの削除設定
remove_pilot_subcarriers = False

# デコーダーの設定
if chip in ['bcm4339', 'bcm43455c0']:
    decoder = 'interleaved'
elif chip in ['bcm4358', 'bcm4366c0']:
    decoder = 'floatingpoint'
else:
    decoder = chip

# ヘルプメッセージ
help_str = f'''
CSI Reader
==========

A simple Python utility to
explore nexmon_csi CSI samples.

Change the config.py to match your
WiFi chip and bandwidth. Current chip
is {chip}.

To explore a sample, type it's
index from the pcap file. Indexes
start from 0.

To plot a range of samples as animation,
type their indexes separated by '-'.

Type 'help' to see this message again.

Type 'exit' to stop this program.
'''