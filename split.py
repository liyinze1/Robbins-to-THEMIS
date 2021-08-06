import os
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='dataset')
parser.add_argument('--valid-ratio', type=float, default=0.2)
parser.add_argument('--prefix', type=str, default='../Robbins-to-THEMIS')
opt = parser.parse_args()

print(opt)

dataset_path = opt.dataset
prefix_path = opt.prefix
valid_ratio = opt.valid_ratio

img_list = [os.sep.join([prefix_path, dataset_path, 'images', img]) + '\n' for img in os.listdir(dataset_path + '/images/')]
random.shuffle(img_list)
train_size = int(len(img_list) * (1 - valid_ratio))

f = open(dataset_path + os.sep + 'train.txt', 'w')
f.writelines(img_list[:train_size])
f.close()

f = open(dataset_path + os.sep + 'valid.txt', 'w')
f.writelines(img_list[train_size:])
f.close()

f = open(dataset_path + os.sep + 'all.txt', 'w')
f.writelines(img_list)
f.close()