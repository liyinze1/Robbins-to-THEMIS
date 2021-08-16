from PIL import Image, ImageOps
import os
from tqdm import tqdm
import argparse


def mirror_or_flip_label(labels: str, key: str):
    res = ''
    global need_id
    for label in labels.splitlines():
        if need_id:
            c, x, y, w, h, id = label.split(' ')
        else:
            c, x, y, w, h = label.split(' ')[:5]
        
        if key == 'h':
            x = str(1 - float(x))
        elif key == 'v':
            y = str(1 - float(y))

        if need_id:
            res += ' '.join((c, x, y, w, h, id))
        else:
            res += ' '.join((c, x, y, w, h))
        res += '\n'
    return res
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default='dataset', help='path to dataset')
    parser.add_argument('--clean', action='store_true', help='de augumentaion')
    parser.add_argument('--no-label', action='store_true')
    parser.add_argument('--no-image', action='store_true')
    parser.add_argument('--id', action='store_true')
    opt = parser.parse_args()

    image_path = opt.dataset + os.sep + 'images' + os.sep
    label_path = opt.dataset + os.sep + 'labels' + os.sep

    if opt.clean:
        os.system('rm -f ' + image_path + '*v.png')
        os.system('rm -f ' + image_path + '*h.png')
        os.system('rm -f ' + label_path + '*v.txt')
        os.system('rm -f ' + label_path + '*h.txt')
        exit()

    global need_id
    no_image = opt.no_image
    no_label = opt.no_label
    need_id = opt.id

    if no_image and no_label:
        exit()

    # read image names
    if no_label:
        image_names = [name[:-4] for name in os.listdir(image_path) if 'v' not in name and 'h' not in name and name.endswith('png')]
    else:
        image_names = [name[:-4] for name in os.listdir(label_path) if 'v' not in name and 'h' not in name and name.endswith('txt')]
    

    for image_name in tqdm(image_names):
        # original image and label
        if not no_label:
            label_file = open(label_path + image_name + '.txt', 'r')
            labels = label_file.read()
            label_file.close()

            label_h = mirror_or_flip_label(labels, 'h')
            label_file_h = open(label_path + image_name + '_h.txt', 'w')
            label_file_h.write(label_h)
            label_file_h.close()

            label_v = mirror_or_flip_label(labels, 'v')
            label_file_v = open(label_path + image_name + '_v.txt', 'w')
            label_file_v.write(label_v)
            label_file_v.close()

            label_vh = mirror_or_flip_label(label_h, 'v')
            label_file_vh = open(label_path + image_name + '_vh.txt', 'w')
            label_file_vh.write(label_vh)
            label_file_vh.close()

        if not no_image:
            image = Image.open(image_path + image_name + '.png')

            image_h = ImageOps.mirror(image)
            image_h.save(image_path + image_name + '_h.png')

            image_v = ImageOps.flip(image)
            image_v.save(image_path + image_name + '_v.png')

            image_vh = ImageOps.flip(image_h)
            image_vh.save(image_path + image_name + '_vh.png')