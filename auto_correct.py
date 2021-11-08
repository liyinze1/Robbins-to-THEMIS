import os
from tqdm import tqdm
import pandas as pd
from utils import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--gt', type=str, default='dataset/labels_0')
parser.add_argument('--yolo', type=str, default='../yolov5/runs\detect\global1-v5m-1\labels')
parser.add_argument('--result', type=str, default='dataset/labels_new')
parser.add_argument('--iou', type=float, default=0.2)
parser.add_argument('--conf', type=float, default=1)
opt = parser.parse_args()

print(opt)

gt_data_path = opt.gt + '/'
yolo_data_path = opt.yolo + '/'
result_path = opt.result + '/'

iou_threshold = opt.iou
conf_threshold = opt.conf

os.system('mkdir %s' % result_path.replace('/', os.sep))

file_list = [name for name in os.listdir(gt_data_path) if name[-3:] == 'txt']

conf_list = []
iou_list = []

for file_name in tqdm(file_list):

    gt_labels = read_labels(gt_data_path + file_name)

    yolo_labels = read_labels(yolo_data_path + file_name, conf=True)
    
    buffer = ''

    for gt_box in gt_labels:

        max_iou, max_iou_box = find_max_iou_box(gt_box, yolo_labels)

        if max_iou > iou_threshold and 0.5 < area(*max_iou_box[:4]) / area(*gt_box) < 2:
            box = max_iou_box
            yolo_labels.remove(max_iou_box)
            iou_list.append(max_iou)
            conf_list.append(box[4])
        else:
            box = gt_box
            
        buffer += '0 ' + ' '.join(xyxy2xywh(*box[: 4], dtype=str)) + '\n'

    for box in yolo_labels:
        if box[4] > conf_threshold:
            buffer += '0 ' + ' '.join(xyxy2xywh(*box[: 4], dtype=str)) + '\n'

    f = open(result_path + file_name, 'w')
    f.write(buffer)
    f.close()

count = pd.DataFrame({'iou': iou_list, 'conf': conf_list})
count.to_csv(result_path + 'count.csv'.replace('/', os.sep))