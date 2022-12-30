import tqdm
import os
import torch
from PIL import Image
from core import imresize
from torchvision import transforms

to_tensor = transforms.ToTensor()
to_pil = transforms.ToPILImage()


def read_batch(d_path, batch_names) -> torch.Tensor:
    torch_imgs = []
    for img_name in batch_names:
        img_path = os.path.join(d_path, img_name)
        img = Image.open(img_path)
        torch_imgs.append(to_tensor(img))
    batch_data = torch.stack(torch_imgs, 0)
    return batch_data


def write_batch(new_d_path, batch_names, batch_data):
    if not os.path.exists(new_d_path):
        os.mkdir(new_d_path)
    for index, img_name in enumerate(batch_names):
        img_path = os.path.join(new_d_path, img_name)
        torch_img = batch_data[index]
        pil_img = to_pil(torch_img)
        pil_img.save(img_path)


def resize_batch(batch_data: torch.Tensor, scale=0.5) -> torch.Tensor:
    batch_data_ds = imresize(batch_data, scale, kernel='cubic')
    return batch_data_ds


def resize_one_directory(d_path, new_d_path, batch_size=8):
    img_names = os.listdir(d_path)
    for i in range(0, len(img_names), batch_size):
        batch_names = []
        for j in range(batch_size):
            if i + j >= len(img_names):
                break
            batch_names.append(img_names[i + j])
        batch_data = read_batch(d_path, batch_names)
        ds_batch_data = resize_batch(batch_data).clamp_(0, 1)
        write_batch(new_d_path, batch_names, ds_batch_data)


def resize_one_class(c_path, new_c_path):
    d_names = os.listdir(c_path)
    new_d_names = []
    d_name_split_list = [d_name.split('_') for d_name in d_names]
    for d_name_split in d_name_split_list:
        if len(d_name_split) == 3:
            name, resolution_raw, fps = d_name_split
            crop = False
        else:
            name, resolution_raw, fps, _ = d_name_split
            crop = True
        width, height = resolution_raw.split('x')
        new_w, new_h = int(width) // 2, int(height) // 2
        new_d_name = name + '_{}' + 'x' + '{}_' + fps
        new_d_name = new_d_name.format(new_w, new_h)
        if crop:
            new_d_name += '_crop'
        new_d_names.append(new_d_name)
    # resize_one_directory
    if not os.path.exists(new_c_path):
        os.mkdir(new_c_path)
    for index, d_name in enumerate(d_names):
        d_path = os.path.join(c_path, d_name)
        new_d_path = os.path.join(new_c_path, new_d_names[index])
        resize_one_directory(d_path, new_d_path)


def resize_hevc(root_path, new_path):
    for class_name in os.listdir(root_path):
        c_path = os.path.join(root_path, class_name)
        new_c_path = os.path.join(new_path, class_name)
        resize_one_class(c_path, new_c_path)


if __name__ == '__main__':
    resize_hevc('E:\dataset\HEVC', 'E:\dataset\HEVC_ds')
