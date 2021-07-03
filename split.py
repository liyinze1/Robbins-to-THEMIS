valid_ratio = 0.2

import os
import random

os.system('move "valid/images\\*.*" "dataset/images/"')
os.system('move "valid/labels\\*.*" "dataset/labels/"')

names = [name[: -4] for name in os.listdir('dataset/images/')]
random.shuffle(names) 
valid_size = int(len(names) * valid_ratio)

for name in names[: valid_size]:
    os.system('move "dataset/images\\%s.png" "valid/images/"' % name)
    os.system('move "dataset/labels\\%s.txt" "valid/labels/"' % name)
