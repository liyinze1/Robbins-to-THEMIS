import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, default='./dataset/labels')
opt = parser.parse_args()
print(opt)

label_path = opt.path.replace('/', os.sep)

names = [name for name in os.listdir(label_path) if name.endswith('txt')]

size = len(names)
count = 0

for name in names:
    f = open(label_path + os.sep + name, 'r')
    count += len(f.read().splitlines())
    f.close()


print('in ' + label_path)
print('total craters:', count)
print('total images:', size)
print('craters per image:', count/size)