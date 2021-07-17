from PIL import Image, ImageOps
import os
from tqdm import tqdm

image_path = 'dataset/images/'
label_path = 'dataset/revised_labels/'

def mirror_or_flip_label(labels: str, key: str):
    res = ''
    for label in labels.splitlines():
        c, x, y, w, h, id = label.split(' ')
        if key == 'h':
            x = str(1 - float(x))
        elif key == 'v':
            y = str(1 - float(y))
        res += ' '.join((c, x, y, w, h, id))
        res += '\n'
    return res
    
if __name__ == '__main__':
    # read image names
    image_names = [name[:-4] for name in os.listdir(image_path) if 'v' not in name and 'h' not in name]

    for image_name in tqdm(image_names):
        # original image and label
        label_file = open(label_path + image_name + '.txt', 'r')
        labels = label_file.read()
        label_file.close()
        image = Image.open(image_path + image_name + '.png')

        # horizontal mirror
        image_h = ImageOps.mirror(image)
        image_h.save(image_path + image_name + '_h.png')
        label_h = mirror_or_flip_label(labels, 'h')
        label_file_h = open(label_path + image_name + '_h.txt', 'w')
        label_file_h.write(label_h)
        label_file_h.close()

        # vertical flip
        image_v = ImageOps.flip(image)
        image_v.save(image_path + image_name + '_v.png')
        label_v = mirror_or_flip_label(labels, 'v')
        label_file_v = open(label_path + image_name + '_v.txt', 'w')
        label_file_v.write(label_v)
        label_file_v.close()

        # mirror and flip
        image_vh = ImageOps.flip(image_h)
        image_vh.save(image_path + image_name + '_vh.png')
        label_vh = mirror_or_flip_label(label_h, 'v')
        label_file_vh = open(label_path + image_name + '_vh.txt', 'w')
        label_file_vh.write(label_vh)
        label_file_vh.close()

