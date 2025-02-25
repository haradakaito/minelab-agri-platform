# 使用するWiFiチップの設定
# --------------------------------------------------
# chip = 'bcm4339'    # Nexus 5
chip = 'bcm43455c0'   # Raspberry Pi 3B+ および 4B
# chip = 'bcm4358'    # Nexus 6P
# chip = 'bcm4366c0'  # Asus RT-AC86U

pcap_fileroot = 'pcapfiles'

bandwidths = ['20', '40', '80', '160']

remove_null_subcarriers  = True
remove_pilot_subcarriers = False

# デコーダ設定
if chip in ['bcm4339', 'bcm43455c0']:
    decoder = '_interleaved'
elif chip in ['bcm4358', 'bcm4366c0']:
    decoder = 'floatingpoint'
else:
    decoder = chip