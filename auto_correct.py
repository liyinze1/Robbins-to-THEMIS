import os
from tqdm import tqdm
import pandas as pd

gt_data_path = '2e/gt_labels/'
yolo_data_path = '2e/0_labels/'
result_path = gt_data_path.replace('labels', 'new_labels')

iou_threshold = 0.2
conf_threshold = 0.9

os.system('mkdir %s' % result_path)

file_list = [name for name in os.listdir(gt_data_path) if name[-3:] == 'txt']

def xyxy2xywh(x1, y1, x2, y2, dtype=float, scale=1):
    x1, y1, x2, y2 = float(x1) * scale, float(y1) * scale, float(x2) * scale, float(y2) * scale
    return dtype((x1 + x2) / 2), dtype((y1 + y2) / 2), dtype(abs(x2 - x1)), dtype(abs(y2 - y1))

def xywh2xyxy(x, y, w, h, dtype=float, scale=1):
    x, y, w, h = float(x) * scale, float(y) * scale, float(w) * scale, float(h) * scale
    return dtype(x - w / 2), dtype(y - h / 2), dtype(x + w / 2), dtype(y + h / 2)

# calculate area of a box
def area(x1, y1, x2, y2):
    return (x2 - x1) * (y2 - y1)

# calculate iou of two boxes
def iou(box1, box2):
    '''
    box1 = [x1, y1, x2, y2]
    box2 = [x1, y1, x2, y2]
    '''
    # calculate intersection
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    # no overlap
    if x1 > x2 or y1 > y2:
        return 0.
    
    intersection_area = area(x1, y1, x2, y2)
    union_area = area(*box1) + area(*box2) - intersection_area
    
    return intersection_area / union_area

# find box with best iou
def find_max_iou_box(box, box_list):
    '''
    box = [x1, x2, x3, x4]
    box_list = [box1, box2, ...]
    '''
    if len(box_list) == 0:
        return 0, None

    max_iou = 0
    max_iou_box = None

    for candi in box_list:
        this_iou = iou(box[:4], candi[:4])
        if this_iou > max_iou:
            max_iou = this_iou
            max_iou_box = candi
    
    return max_iou, max_iou_box

conf_list = []
iou_list = []

for file_name in tqdm(file_list):

    f = open(gt_data_path + file_name, 'r')
    gt_labels = [xywh2xyxy(*label.split()[1: 5]) for label in f.read().splitlines()]
    f.close()

    try:
        f = open(yolo_data_path + file_name, 'r')
        yolo_labels = [list(xywh2xyxy(*label.split()[1: 5])) + [float(label.split()[5])] for label in f.read().splitlines()]
        f.close()
    except:
        yolo_labels = []
    
    buffer = ''

    for gt_box in gt_labels:

        max_iou, max_iou_box = find_max_iou_box(gt_box, yolo_labels)
        
        area_scale = area(max_iou_box) / area(gt_box)

        if 0.5 < area_scale < 2 and max_iou > iou_threshold:
            box = max_iou_box
            yolo_labels.remove(max_iou_box)
            iou_list.append(max_iou)
            conf_list.append(box[4])
        else:
            box = gt_box
            
        buffer += '0 ' + ' '.join(xyxy2xywh(*box[: 4], dtype=str)) + '\n'

    for box in yolo_labels:
        if box[5] > conf_threshold:
            buffer += '0 ' + ' '.join(xyxy2xywh(*box[: 4], dtype=str)) + '\n'

    f = open(result_path + file_name, 'w')
    f.write(buffer)
    f.close()

count = pd.DataFrame({'iou': iou_list, 'conf': conf_list})
count.to_csv(gt_data_path.replace('labels', '') + 'count.csv')