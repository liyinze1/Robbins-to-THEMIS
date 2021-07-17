valid_ratio = 0.2

import os
import random
import platform


if platform.system().lower() == 'windows':
    slash = '\\'
    mv_cmd = 'move'
else:
    slash = '/'
    mv_cmd = 'mv'

os.system('mkdir valid')
os.system('mkdir valid' + slash + 'images')
os.system('mkdir valid' + slash + 'labels')

names = [name[: -4] for name in os.listdir('dataset/images/')]
random.shuffle(names) 
valid_size = int(len(names) * valid_ratio)

os.system('%s "valid/images%s*.*" "dataset/images/"' % (mv_cmd, slash))
os.system('%s "valid/labels%s*.*" "dataset/labels/"' % (mv_cmd, slash))
for name in names[: valid_size]:
    os.system('%s "dataset/images%s%s.png" "valid/images/"' % (mv_cmd, slash, name))
    os.system('%s "dataset/labels%s%s.txt" "valid/labels/"' % (mv_cmd, slash, name))
