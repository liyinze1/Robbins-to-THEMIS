valid_ratio = 0.2

import os
import random

dataset_path = 'combined_dataset'
prefix_path = '../'

img_list = [prefix_path + dataset_path + '/images/' + img + '\n' for img in os.listdir(dataset_path + '/images/')]
random.shuffle(img_list)
train_size = int(len(img_list) * (1 - valid_ratio))

f = open('train.txt', 'w')
f.writelines(img_list[:train_size])
f.close()

f = open('valid.txt', 'w')
f.writelines(img_list[train_size:])
f.close()

f = open('test.txt', 'w')
f.writelines(img_list)
f.close()