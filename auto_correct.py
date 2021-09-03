import os
from tqdm import tqdm
import pandas as pd
from utils import *

gt_data_path = 'dataset/4_labels/'
yolo_data_path = '../yolov5/runs/detect/global_5/labels/'
result_path = gt_data_path.replace('labels', 'new_labels')

iou_threshold = 0.2
conf_threshold = 1

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
count.to_csv('dataset/count.csv')