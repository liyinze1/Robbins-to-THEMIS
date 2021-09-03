
from os import error

def average_two_box(box1, box2):
    return [(n + m) / 2 for n, m in zip(box1, box2)]
    
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

def read_labels(filename, scale=1, id=False, conf=False):
    try:
        f = open(filename, 'r')
        if id:
            labels = []
            for line in f.read().splitlines():
                label = list(xywh2xyxy(*line.split()[1: 5], scale=scale))
                if len(line.split()) == 6:
                    id = label.split()[5]
                else:
                    id = ''
                label.append(id)
                labels.append(label)
        elif conf:
            labels = [list(xywh2xyxy(*label.split()[1: 5], scale=scale)) + [float(label.split()[5])] for label in f.read().splitlines()]
        else:
            labels = [xywh2xyxy(*label.split()[1: 5], scale=scale) for label in f.read().splitlines()]
        f.close()
    except error:    
        labels = []
        print(error)
    
    return labels