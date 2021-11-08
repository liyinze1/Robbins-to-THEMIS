import os
from tqdm import tqdm
import pandas as pd
from utils import *
import argparse
from math import cos, radians
import numpy as np
import matplotlib.pyplot as plt
import threading

parser = argparse.ArgumentParser()
parser.add_argument('--gt', type=str, default='dataset/labels')
parser.add_argument('--detect', type=str, default='../yolov5/runs/detect/combined-v5s-new/labels')
parser.add_argument('--iou', type=float, default=0.2)
parser.add_argument('--conf', type=float, default=1)
parser.add_argument('--lat', type=int, default=0)
parser.add_argument('--threads', type=int, default=6)

opt = parser.parse_args()

print(opt)

gt_data_path = opt.gt + '/'
yolo_data_path = opt.detect + '/'
iou_threshold = opt.iou
conf_threshold = opt.conf
lat_threshold = opt.lat
n_thread = opt.threads

size_range = (15, 100)

lock = threading.Lock()

def accounting(label_names):
    global tp
    global fp
    global fn

    local_tp = []
    local_fp = []
    local_fn = 0
    for name in tqdm(label_names):
        lat = int(name.split('_')[0])

        w_scale = cos(radians(lat))

        gt_boxes = read_labels(gt_data_path + name, scale=593)
        gt_boxes = box_filter(gt_boxes, size_range, w_scale, keep_boundary_box=True)

        yolo_boxes = read_labels(yolo_data_path + name, scale=593, conf=True)

        for box in gt_boxes:
            max_iou, max_iou_box = find_max_iou_box(box, yolo_boxes)
            if max_iou > iou_threshold:
                local_tp.append(max_iou_box[-1])
                yolo_boxes.remove(max_iou_box)
            else:
                local_fn += 1
        
        for box in box_filter(yolo_boxes, size_range, w_scale, keep_boundary_box=False):
            local_fp.append(box[-1])

    lock.acquire()
    tp += local_tp
    fp += local_fp
    fn += local_fn
    lock.release()

tp = []
fp = []
fn = 0
label_names = [name for name in os.listdir(gt_data_path) if name[-3:] == 'txt' if abs(int(name.split('_')[0])) >= lat_threshold]
thread_list = []
thread_args = list_to_thread_list(label_names, n_thread)

for thread_arg in thread_args:
    thread = threading.Thread(target=accounting, args=(thread_arg, ))
    thread.start()
    thread_list.append(thread)

for thread in thread_list:
    thread.join()

print('\n'*n_thread)
print('----------done------------')

tp.sort()
fp.sort()

len_tp = len(tp)
len_fp = len(fp)

n_crater = len_tp + fn

confs = np.linspace(0, 1, 100)
tp_y = np.empty(100)
fp_y = np.empty(100)
fn_y = np.empty(100)

tp_i = 0
fp_i = 0

for i, conf in enumerate(confs):
    while tp_i < len_tp and tp[tp_i] < conf:
        tp_i += 1
    while fp_i < len_fp and fp[fp_i] < conf:
        fp_i += 1

    current_tp = len_tp - tp_i
    current_fp = len_fp - fp_i
    current_fn = n_crater - current_tp

    tp_y[i] = current_tp
    fp_y[i] = current_fp
    fn_y[i] = current_fn

tpr = tp_y / (tp_y + fn_y)
print('true positive rate:', max(tpr))

result_path = './test/' + yolo_data_path.strip('/').split('/')[-2]
if lat_threshold != 0:
    result_path += '_lat%d'%lat_threshold
os.system('mkdir ' + result_path.replace('/', os.sep))

table = pd.DataFrame({'conf': confs, 'tp': tp_y, 'fp': fp_y, 'fn': fn_y, 'tpr': tpr})
table.to_csv(result_path + '/' + 'table.csv'.replace('/', os.sep))

plt.figure(figsize=(10,4))
plt.subplot(1, 2, 1)
plt.plot(confs, tp_y, label='tp')
plt.plot(confs, fp_y, label='fp')
plt.plot(confs, fn_y, label='fn')
plt.legend()
plt.grid()
plt.xlabel('confidence')

plt.subplot(1, 2, 2)
plt.plot(confs, tpr, label='true positive rate')
plt.legend()
plt.grid()
plt.xlabel('confidence')

plt.savefig(result_path + '/' + 'plot.svg'.replace('/', os.sep))