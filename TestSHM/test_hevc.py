import os
import re
import numpy as np
import math
import json
from tqdm import tqdm
from PIL import Image


def psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))


def psnr_between_pic(img1_path, img2_path):
    img1 = np.array(Image.open(img1_path))
    img2 = np.array(Image.open(img2_path))
    quality_psnr = psnr(img1, img2)
    return quality_psnr


def encode_one_sequence(s_path, s_path_ds, new_s_path, qp_list=None, gop_size=12, frame_to_encode=36):
    if qp_list is None:
        qp_list = [37, 32, 27, 22]
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
    FrameRate0 = int(fps)
    SourceWidth0 = width // 2
    SourceHeight0 = height // 2

    InputFile1 = s_path
    FrameRate1 = int(fps)
    SourceWidth1 = width
    SourceHeight1 = height

    base_command = 'TAppEncoderStatic -c cfg/low_delay_P_scalable.cfg -c cfg/spatial444.cfg -c cfg/layers.cfg'
    gop_command = f' -ip0 {gop_size} -ip1 {gop_size} -f {frame_to_encode}'
    input_command = f' -i0 {InputFile0} -fr0 {FrameRate0} -wdt0 {SourceWidth0} -hgt0 {SourceHeight0}' \
                    f' -i1 {InputFile1} -fr1 {FrameRate1} -wdt1 {SourceWidth1} -hgt1 {SourceHeight1}'
    if not os.path.exists(new_s_path):
        os.mkdir(new_s_path)

    a_part = "a\\s+[-+]?[0-9]*\.[0-9]+"
    p_part = "p\\s+[-+]?[0-9]*\.[0-9]+"
    i_part = "i\\s+[-+]?[0-9]*\.[0-9]+"

    BL_a_bpps = []
    BL_p_bpps = []
    BL_i_bpps = []
    EL_a_bpps = []
    EL_p_bpps = []
    FL_a_bpps = []
    FL_p_bpps = []
    for qp in qp_list:
        qp_command = f' -q0 {qp} -q1 {qp}'
        output_command = f' -b {new_s_path}/{qp}.bin -o0 {new_s_path}/{qp}_BL.yuv -o1 {new_s_path}/{qp}_EL.yuv'
        full_command = base_command + gop_command + input_command + qp_command + output_command
        output = os.popen(full_command).read()
        all_bitrate = re.findall(a_part, output)
        p_bitrate = re.findall(p_part, output)
        i_bitrate = re.findall(i_part, output)

        BL_a_bitrate = float(all_bitrate[0][1:].lstrip())
        EL_a_bitrate = float(all_bitrate[1][1:].lstrip())
        BL_p_bitrate = float(p_bitrate[0][1:].lstrip())
        EL_p_bitrate = float(p_bitrate[1][1:].lstrip())
        BL_i_bitrare = float(i_bitrate[0][1:].lstrip())

        BL_a_bpp = BL_a_bitrate * 1000 / (FrameRate0 * SourceWidth0 * SourceHeight0)
        BL_p_bpp = BL_p_bitrate * 1000 / (FrameRate0 * SourceWidth0 * SourceHeight0)
        BL_i_bpp = BL_i_bitrare * 1000 / (FrameRate0 * SourceWidth0 * SourceHeight0)
        EL_a_bpp = EL_a_bitrate * 1000 / (FrameRate1 * SourceWidth1 * SourceHeight1)
        EL_p_bpp = EL_p_bitrate * 1000 / (FrameRate1 * SourceWidth1 * SourceHeight1)
        FL_a_bpp = (BL_a_bpp * SourceWidth0 * SourceHeight0 + EL_a_bpp * SourceWidth1 * SourceHeight1) / (SourceWidth1 * SourceHeight1)
        FL_p_bpp = (BL_p_bpp * SourceWidth0 * SourceHeight0 + EL_p_bpp * SourceWidth1 * SourceHeight1) / (SourceWidth1 * SourceHeight1)

        BL_a_bpps.append(BL_a_bpp)
        BL_p_bpps.append(BL_p_bpp)
        BL_i_bpps.append(BL_i_bpp)
        EL_a_bpps.append(EL_a_bpp)
        EL_p_bpps.append(EL_p_bpp)
        FL_a_bpps.append(FL_a_bpp)
        FL_p_bpps.append(FL_p_bpp)

    # write to json
    sequence_dict_base = {}
    sequence_dict_enhance = {}
    sequence_dict_full = {}
    for i in range(len(qp_list)):
        model_dict_base = {}
        model_dict_enhance = {}
        model_dict_full = {}

        model_dict_base['i_frame_num'] = (frame_to_encode - 1) // gop_size + 1
        model_dict_base['p_frame_num'] = frame_to_encode - ((frame_to_encode - 1) // gop_size + 1)
        model_dict_base['ave_i_frame_bpp'] = BL_i_bpps[i]
        model_dict_base['ave_i_frame_quality'] = 0.0
        model_dict_base['ave_p_frame_bpp'] = BL_p_bpps[i]
        model_dict_base['ave_p_frame_quality'] = 0.0
        model_dict_base['ave_all_frame_bpp'] = BL_a_bpps[i]
        model_dict_base['ave_all_frame_quality'] = 0.0

        model_dict_enhance['i_frame_num'] = 0
        model_dict_enhance['p_frame_num'] = frame_to_encode
        model_dict_enhance['ave_i_frame_bpp'] = 0.0
        model_dict_enhance['ave_i_frame_quality'] = 0.0
        model_dict_enhance['ave_p_frame_bpp'] = EL_p_bpps[i]
        model_dict_enhance['ave_p_frame_quality'] = 0.0
        model_dict_enhance['ave_all_frame_bpp'] = EL_a_bpps[i]
        model_dict_enhance['ave_all_frame_quality'] = 0.0

        model_dict_full['i_frame_num'] = (frame_to_encode - 1) // gop_size + 1
        model_dict_full['p_frame_num'] = frame_to_encode - ((frame_to_encode - 1) // gop_size + 1)
        model_dict_full['ave_i_frame_bpp'] = BL_i_bpps[i]
        model_dict_full['ave_i_frame_quality'] = 0.0
        model_dict_full['ave_p_frame_bpp'] = FL_p_bpps[i]
        model_dict_full['ave_p_frame_quality'] = 0.0
        model_dict_full['ave_all_frame_bpp'] = FL_a_bpps[i]
        model_dict_full['ave_all_frame_quality'] = 0.0

        sequence_dict_base[f'{qp_list[i]}.model'] = model_dict_base
        sequence_dict_enhance[f'{qp_list[i]}.model'] = model_dict_enhance
        sequence_dict_full[f'{qp_list[i]}.model'] = model_dict_full

    return sequence_dict_base, sequence_dict_enhance, sequence_dict_full


def calculate_sequence_psnr(gt_path, rec_path, qp_list=None, layer: str = '', gop_size=12):
    """
    Args:
        layer: BL or EL
        qp_list: qp setting
        gt_path: ground trurt rgb images' path
        rec_path: rec .yuv path

    Returns:
        several qp's corrosponding psnr quality
    """
    if qp_list is None:
        qp_list = [37, 32, 27, 22]
    if layer == '':
        layer = 'BL'

    sequence_dict = {}
    for qp in tqdm(qp_list, ncols=10, position=0):
        model_dict = {}
        rec_yuv = f'{qp}_{layer}.yuv'
        cd_command = "cd {} && "
        mkdir_command = "mkdir {} && "
        yuv2png_command = "ffmpeg -pix_fmt yuv444p -loglevel quiet -s {} -i {}.yuv -f image2 {}/im%05d.png"
        qp_dir_name = f'{qp}_{layer}'
        resolution = os.path.split(rec_path)[1].split('_')[1]

        yuv2png_command = cd_command.format(rec_path) + mkdir_command.format(qp_dir_name) + yuv2png_command.format(resolution, rec_yuv, qp_dir_name)
        os.system(yuv2png_command)
        # calculate psnr with gt
        rec_img_names = os.listdir(os.path.join(rec_path, qp_dir_name))
        psnr_i_sum = 0
        psnr_p_sum = 0
        frame_num = len(rec_img_names)
        print(f'QP:{qp} -> Frame num:{frame_num}')
        for index, img_name in enumerate(rec_img_names):
            if index % gop_size == 0 and layer == 'BL':
                img1_path = os.path.join(gt_path, img_name)
                img2_path = os.path.join(rec_path, qp_dir_name, img_name)
                psnr = psnr_between_pic(img1_path, img2_path)
                psnr_i_sum += psnr
            else:
                img1_path = os.path.join(gt_path, img_name)
                img2_path = os.path.join(rec_path, qp_dir_name, img_name)
                psnr = psnr_between_pic(img1_path, img2_path)
                psnr_p_sum += psnr
        if layer == 'BL':
            i_num = (frame_num - 1) // gop_size + 1
        else:
            i_num = 0
        p_num = frame_num - i_num
        psnr_i_avg = psnr_i_sum / i_num
        psnr_p_avg = psnr_p_sum / p_num
        psnr_a_avg = (psnr_i_sum + psnr_p_sum) / frame_num

        # write into dict
        model_dict['ave_i_frame_quality'] = psnr_i_avg
        model_dict['ave_p_frame_quality'] = psnr_p_avg
        model_dict['ave_all_frame_quality'] = psnr_a_avg
        sequence_dict[f'{qp}.model'] = model_dict

        print(f'QP:{qp} -> average all-psnr:{psnr_a_avg}')
    return sequence_dict


if __name__ == '__main__':
    encode_one_sequence('/home/esakak/dataset/HEVC_yuv444/ClassD/BasketballPass_416x240_50.yuv',
                        '/home/esakak/dataset/HEVC_yuv444_ds/ClassD/BasketballPass_208x120_50.yuv',
                        '/home/esakak/dataset/HEVC_yuv444_compress/ClassD/BasketballPass_416x240_50')
