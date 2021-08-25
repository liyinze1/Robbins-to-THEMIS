import tkinter as tk
import os
import random
import cv2
from PIL import Image, ImageTk
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='dataset')
parser.add_argument('--shuffle', action='store_true')
parser.add_argument('--line', type=int, default=1, help='line width')
opt = parser.parse_args()
print(opt)

slash = os.sep
image_path = (opt.dataset + '/images/').replace('/', slash)
label_path = (opt.dataset + '/labels/').replace('/', slash)
color = (0, 255, 0)
line_width = opt.line
shuffle = True

img_list = [img for img in os.listdir(image_path) if img.endswith(('png', 'jpg', 'jpeg'))]
img_format = img_list[0].split('.')[-1]
if opt.shuffle:
    random.shuffle(img_list)

img_idx = -1
img_len = len(img_list)

window = tk.Tk()
tk_label = tk.Label(window)
tk_label.pack(padx=10, pady=10) 

def xywh2xyxy(x, y, w, h, dtype=float, scale=(1, 1)):
    x, y, w, h = float(x) * scale[0], float(y) * scale[1], float(w) * scale[0], float(h) * scale[1]
    return dtype(x - w / 2), dtype(y - h / 2), dtype(x + w / 2), dtype(y + h / 2)

def show_next():
    global img_idx
    global img_list
    global tk_label
    global tk_img
    global img

    img_idx += 1
    if img_idx == img_len:
        exit()

    tk_label.destroy()


    img_name = img_list[img_idx]
    lbl_name = img_name.replace(img_format, 'txt')

    window.title('%d/%d, %s' % (img_idx + 1, img_len, img_name))

    img = cv2.imread(image_path + slash + img_name)

    img_shape = img.shape

    try:
        f = open(label_path + lbl_name, 'r')
        label_list = [line.split(' ') for line in f.read().splitlines()]
        f.close()
    except:
        label_list = []
    
    for label in label_list:
        x1, y1, x2, y2 = xywh2xyxy(*label[1:5], dtype=round, scale=img_shape[:2])
        cv2.rectangle(img, (x1, y1), (x2, y2), color, line_width)
    
    pillow_img = Image.fromarray(img[:,:,::-1])
    tk_img = ImageTk.PhotoImage(image=pillow_img)
    tk_label = tk.Label(window, image=tk_img)
    tk_label.pack(padx=10, pady=10) 

show_next()

next_set = set(['bracketright', 'Down', 'Right', 'Return'])
last_set = set(['bracketleft', 'Left', 'Up'])

def keyboard_action(event):
    key = event.keysym
    if key in last_set:
        global img_idx
        if img_idx > 0:
            img_idx -= 2
            show_next()
    elif key in next_set:
        show_next()
    elif key == 's':
        cv2.imwrite(img_list[img_idx] + '.png', img)
window.bind('<Key>', keyboard_action)

window.mainloop()