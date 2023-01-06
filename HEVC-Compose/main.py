import os
from tqdm import tqdm


def compose_one_sequence(s_path, new_s_path):
    _, name = os.path.split(s_path)
    name_splits = name.split('_')
    if len(name_splits) == 3:
        name, resolution_raw, fps = name_splits
    else:
        name, resolution_raw, fps, _ = name_splits
    cd_command = f'cd {s_path}'
    compose_command = f'ffmpeg -r {fps} -i im%5d.png -pix_fmt yuv420p -s {resolution_raw} {new_s_path}.yuv'
    full_command = cd_command + '&' + compose_command
    os.system(full_command)
    print(name)


def compose_one_class(c_path, new_c_path):
    if not os.path.exists(new_c_path):
        os.mkdir(new_c_path)
    for s_name in os.listdir(c_path):
        s_path = os.path.join(c_path, s_name)
        new_s_path = os.path.join(new_c_path, s_name)
        compose_one_sequence(s_path, new_s_path)


def compose_hevc(root_path, new_path):
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    for c_name in tqdm(os.listdir(root_path)):
        c_path = os.path.join(root_path, c_name)
        new_c_path = os.path.join(new_path, c_name)
        compose_one_class(c_path, new_c_path)


if __name__ == '__main__':
    compose_hevc('E:\dataset\For420T\HEVC_ds', 'E:\dataset\For420T\HEVC_yuv420_ds')
