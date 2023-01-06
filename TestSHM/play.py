# import os
# import re
#
# output = """
# SUMMARY --------------------------------------------------------
#         Total Frames |   Bitrate     Y-PSNR    U-PSNR    V-PSNR    YUV-PSNR
#   L0           36    a      14.6889   25.3854   32.3423   30.6702   28.3795
#   L1           36    a      71.2556   25.2989   26.6796   26.1904   25.8905
#
#
# I Slices--------------------------------------------------------
#         Total Frames |   Bitrate     Y-PSNR    U-PSNR    V-PSNR    YUV-PSNR
#   L0            3    i      92.4000   26.1347   32.0772   31.1328   28.9418
#   L1            0    i         -nan      -nan      -nan      -nan      -nan
#
#
# P Slices--------------------------------------------------------
#         Total Frames |   Bitrate     Y-PSNR    U-PSNR    V-PSNR    YUV-PSNR
#   L0           33    p       7.6242   25.3173   32.3664   30.6281   28.3318
#   L1           36    p      71.2556   25.2989   26.6796   26.1904   25.8905
#
#
# B Slices--------------------------------------------------------
#         Total Frames |   Bitrate     Y-PSNR    U-PSNR    V-PSNR    YUV-PSNR
#   L0            0    b         -nan      -nan      -nan      -nan      -nan
#   L1            0    b         -nan      -nan      -nan      -nan      -nan
#
# RVM[L0]: 0.000
# RVM[L1]: 0.000
#
# Bytes written to file: 12150 (135.000 kbps)
# """
# a_part = "a\\s+[-+]?[0-9]*\.[0-9]+"
# p_part = "p\\s+[-+]?[0-9]*\.[0-9]+"
# all_bitrate = re.findall(a_part, output)
# p_bitrate = re.findall(p_part, output)
#
# BL_a_bitrate = float(all_bitrate[0][1:].lstrip())
# EL_a_bitrate = float(all_bitrate[1][1:].lstrip())
# BL_p_bitrate = float(p_bitrate[0][1:].lstrip())
# EL_p_bitrate = float(p_bitrate[1][1:].lstrip())
#
# print(BL_a_bitrate, BL_p_bitrate, EL_a_bitrate, EL_p_bitrate)

import subprocess

p = subprocess.Popen('dir', shell=True)
p.wait()
a = p.stdout.readlines()
print(a)
# print(a.stdout)