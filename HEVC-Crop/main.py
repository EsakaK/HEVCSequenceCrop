# generating sequences from HEVC test

import os
import sys

from tqdm import tqdm


def main(argv):
    hevc_root_path = "E:\dataset\For420T\HEVC_yuv420_ds"  # the line you need to change
    cd_command = "cd {} && "
    crop_command = "ffmpeg -pix_fmt yuv420p  -s {} -i  {} -vf crop={}:0:0 {}"
    mkdir_command = "mkdir {}"
    yuv2png_command = "ffmpeg -pix_fmt yuv420p -s {} -i {}.yuv -f image2 {}/im%05d.png"
    hevc_dirs = [dir_name for dir_name in os.listdir(hevc_root_path) if "Class" in dir_name]
    for dir_name in tqdm(hevc_dirs):
        print(dir_name)
        class_path = os.path.join(hevc_root_path, dir_name)
        yuv_file_list = os.listdir(class_path)
        yuv_file_split_list = [yuv_file[:-4].split('_') for yuv_file in yuv_file_list if
                               os.path.isfile(os.path.join(class_path, yuv_file))]
        print(yuv_file_split_list)
        for yuv_file_split in yuv_file_split_list:
            if len(yuv_file_split) == 3:
                name, resolution_raw, fps = yuv_file_split
                crop = False
            else:
                name, resolution_raw, fps, _ = yuv_file_split
                crop = True
            width, height = resolution_raw.split('x')
            crop_width, crop_height, flag = return_crop_size(width, height)
            resolution = crop_width + 'x' + crop_height
            crop_size = crop_width + ':' + crop_height
            input_filename_wo_extention = '_'.join(yuv_file_split)
            new_file_name_wo_extention = "_".join([name, resolution, fps])
            if crop:
                new_file_name_wo_extention = new_file_name_wo_extention + '_crop'
            # ffmpeg crop
            cd_command_cur = cd_command.format(class_path)
            crop_command_cur = cd_command_cur + crop_command.format(resolution_raw, input_filename_wo_extention + '.yuv',
                                                                    crop_size,
                                                                    new_file_name_wo_extention + '.yuv')
            print(crop_command_cur)
            if flag:
                os.system(crop_command_cur)
            mkdir_command_cur = cd_command_cur + mkdir_command.format(new_file_name_wo_extention)
            os.system(mkdir_command_cur)
            yuv2png_command_cur = cd_command_cur + yuv2png_command.format(resolution, new_file_name_wo_extention,
                                                                          new_file_name_wo_extention)
            os.system(yuv2png_command_cur)


def return_crop_size(width, height, size=64, crop_flag=False):
    """
    Args:
        size: minimal crop size

    Returns: croped size
    """
    width = int(width)
    height = int(height)
    if not crop_flag:
        crop_width = width
        crop_height = height
    else:
        crop_width = width // size * size
        crop_height = height // size * size
    if crop_height == height and crop_width == width:
        flag = False
    else:
        flag = True
    return str(crop_width), str(crop_height), flag


if __name__ == '__main__':
    main(sys.argv)
