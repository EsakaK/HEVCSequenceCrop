import os
import re
import json

command = 'SHMEnc -c cfg/low_delay_P_scalable.cfg -c cfg/spatial444.cfg -c cfg/layers.cfg -q0 22 -q1 22 -b str/test.bin -o0 rec/test.yuv -o1 rec/test1.yuv'


def encode_one_sequence(s_path, s_path_ds, new_s_path):
    qp_list = [48]
    file_name = os.path.split(s_path)[1][:-4]
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

    base_command = 'TAppEncoderStatic -c cfg/low_delay_P_scalable.cfg -c cfg/spatial444.cfg -c cfg/layers.cfg'
    input_command = f' -i0 {InputFile0} -fr0 {FrameRate0} -wdt0 {SourceWidth0} -hgt0 {SourceHeight0}' \
                    f' -i1 {InputFile1} -fr1 {FrameRate1} -wdt1 {SourceWidth1} -hgt1 {SourceHeight1}'
    if not os.path.exists(new_s_path):
        os.mkdir(new_s_path)

    a_part = "a\\s+[-+]?[0-9]*\.[0-9]+"
    p_part = "p\\s+[-+]?[0-9]*\.[0-9]+"

    BL_a_bpps = []
    BL_p_bpps = []
    EL_a_bpps = []
    EL_p_bpps = []
    for qp in qp_list:
        qp_command = f' -q0 {qp} -q1 {qp}'
        output_command = f' -b {new_s_path}/{qp}.bin -o0 {new_s_path}/{qp}_BL.yuv -o1 {new_s_path}/{qp}_EL.yuv'
        full_command = base_command + input_command + qp_command + output_command
        output = os.popen(full_command).read()
        all_bitrate = re.findall(a_part, output)
        p_bitrate = re.findall(p_part, output)

        BL_a_bitrate = float(all_bitrate[0][1:].lstrip())
        EL_a_bitrate = float(all_bitrate[1][1:].lstrip())
        BL_p_bitrate = float(p_bitrate[0][1:].lstrip())
        EL_p_bitrate = float(p_bitrate[1][1:].lstrip())

        BL_a_bpp = BL_a_bitrate * 1000 / (fps * SourceWidth0 * SourceHeight0)
        BL_p_bpp = BL_p_bitrate * 1000 / (fps * SourceWidth0 * SourceHeight0)
        EL_a_bpp = EL_a_bitrate * 1000 / (fps * SourceWidth1 * SourceHeight1)
        EL_p_bpp = EL_p_bitrate * 1000 / (fps * SourceWidth1 * SourceHeight1)

        BL_a_bpps.append(BL_a_bpp)
        BL_p_bpps.append(BL_p_bpp)
        EL_a_bpps.append(EL_a_bpp)
        EL_p_bpps.append(EL_p_bpp)

    # write to json
    print(BL_a_bpps)
    print(BL_p_bpps)
    print(EL_a_bpps)
    print(EL_p_bpps)




if __name__ == '__main__':
    encode_one_sequence('/home/esakak/dataset/HEVC_yuv444/ClassD/BasketballPass_416x240_50.yuv',
                        '/home/esakak/dataset/HEVC_yuv444_ds/ClassD/BasketballPass_208x120_50.yuv',
                        '/home/esakak/dataset/HEVC_yuv444_compress/ClassD/BasketballPass_416x240_50')
