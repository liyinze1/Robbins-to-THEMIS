valid_ratio = 0.2

import os
import random
import platform

dataset_path = 'dataset'
valid_path = 'valid'

if platform.system().lower() == 'windows':
    mv_cmd = 'move'
else:
    mv_cmd = 'mv'

slash = os.sep
os.system('mkdir ' + valid_path)
os.system('mkdir ' + valid_path + slash + 'images')
os.system('mkdir ' + valid_path + slash + 'labels')

names = [name[: -4] for name in os.listdir('dataset/images/')]
random.shuffle(names) 
valid_size = int(len(names) * valid_ratio)

os.system('%s "valid/images%s*.*" "%s/images/"' % (mv_cmd, slash, dataset_path))
os.system('%s "valid/labels%s*.*" "%s/labels/"' % (mv_cmd, slash, dataset_path))
for name in names[: valid_size]:
    os.system('%s "dataset/images%s%s.png" "%s/images/"' % (mv_cmd, slash, name, valid_path))
    os.system('%s "dataset/labels%s%s.txt" "%s/labels/"' % (mv_cmd, slash, name, valid_path))
