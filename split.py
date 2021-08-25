import os
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='dataset')
parser.add_argument('--valid', type=float, default=0.2)
parser.add_argument('--test', type=float, default=0.0)
parser.add_argument('--prefix', type=str, default='../Robbins-to-THEMIS/dataset')
opt = parser.parse_args()

print(opt)

dataset_path = opt.dataset
prefix_path = opt.prefix
valid_ratio = opt.valid
test_ratio = opt.test

img_format = ('png', 'jpg', 'jpeg')

img_list = [os.sep.join([prefix_path, 'images', img]) + '\n' for img in os.listdir(dataset_path + '/images/') if img.endswith(img_format)]
random.shuffle(img_list)
valid_index = int(len(img_list) * (1 - valid_ratio - test_ratio))
test_index = int(len(img_list) * (1 - test_ratio))

if valid_index > 0:
    f = open(dataset_path + os.sep + 'train.txt', 'w')
    f.writelines(img_list[:valid_index])
    f.close()

if valid_ratio > 0:
    f = open(dataset_path + os.sep + 'valid.txt', 'w')
    f.writelines(img_list[valid_index:test_index])
    f.close()

if test_ratio > 0:
    f = open(dataset_path + os.sep + 'test.txt', 'w')
    f.writelines(img_list[test_index:])
    f.close()

f = open(dataset_path + os.sep + 'all.txt', 'w')
f.writelines(img_list)
f.close()