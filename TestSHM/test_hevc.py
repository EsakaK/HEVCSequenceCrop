import os
import re
import json

command = 'SHMEnc -c cfg/low_delay_P_scalable.cfg -c cfg/spatial444.cfg -c cfg/layers.cfg -q0 22 -q1 22 -b str/test.bin -o0 rec/test.yuv -o1 rec/test1.yuv'


def encode_one_sequence(s_path, s_path_ds, new_s_path):
    qp_list = [48]
    file_name = os.path.split(s_path)
    name_split = file_name.split('_')
    if len(name_split) == 3:
        name, resolution, fps = name_split
    else:
        name, resolution, fps, _ = name_split
    width, height = resolution.split('x')
    width = int(width)
    height = int(height)
    InputFile0 = s_path_ds
    FrameRate0 = fps
    SourceWidth0 = width // 2
    SourceHeight0 = height // 2

    InputFile1 = s_path
    FrameRate1 = fps
    SourceWidth1 = width
    SourceHeight1 = height

    base_command = 'SHMEnc -c cfg/low_delay_P_scalable.cfg -c cfg/spatial444.cfg -c cfg/layers.cfg '
    for qp in qp_list:
        qp_command = f'-qp0 {qp} -qp1 {qp}'
