import os
import tkinter as tk
import os
import random
from math import cos, radians
from utils import *

resolution = 593
img_path = '2e/images/'
gt_label_image_path = '2e/label_image/'

gt_label_path = '2e/0_4_labels/'
yolo_label_path = '2e/5_labels/'
robbins_label_path = '2e/gt_labels/'

revised_label_path = '2e/revised_labels/'

conf_thresh = 0.5
conf_thresh_up = 1
iou_thresh = 0.5


os.system('mkdir ' + revised_label_path)

# read images
img_names = [name[:-4] for name in os.listdir(img_path) if name[-5] not in ('h', 'v')]

# remove done work from to-do list
done_work_names = set([name[:-4] for name in os.listdir(revised_label_path)])
img_names = [name for name in img_names if name not in done_work_names]


# number of done labels
done_work_num = len(done_work_names)
# number of total labels
total_work_num = len(img_names)

font = ('Courier', 15)

# create window
window = tk.Tk()

'''
    code for yolo canvas on the left
'''
yolo_img_frame = tk.Frame(window, padx=10, pady=10)
yolo_img_frame.pack(side='left')

yolo_canvas = tk.Canvas(yolo_img_frame, bg='lightgray', height=resolution, width=resolution, borderwidth=0, highlightthickness=0)
yolo_canvas.pack()


'''
    code for check button of yolo
'''
yolo_button_frame = tk.Frame(window, padx=10, pady=10)
yolo_button_frame.pack(side='left')


'''
    code for right gt canvas
'''
gt_img_frame = tk.Frame(window, padx=10, pady=10)
gt_img_frame.pack(side='left')

gt_canvas = tk.Canvas(gt_img_frame, bg='lightgray', height=resolution, width=resolution, borderwidth=0, highlightthickness=0)
gt_canvas.pack()


def get_random_color():
    global color_list
    R = G = B = 0
    # avoid gray color
    while max(R, G, B) - min(R, G, B) < 100:
        R = random.randint(60,255)
        G = random.randint(60,255)
        B = random.randint(60,255)
    color = '#' + '%02x'%R + '%02x'%G + '%02x'%B
    return color


'''
    def some list to contain rects and buttons
'''
yolo_button_list = []
yolo_rect_list = []
yolo_button_var_list = []

def yolo_button_action():
    for i, button_var in enumerate(yolo_button_var_list):
        if button_var.get():
            yolo_canvas.itemconfigure(yolo_rect_list[i], state='normal')
        else:
            yolo_canvas.itemconfigure(yolo_rect_list[i], state='hidden')


label_list = []
img_idx_stack = []

# save labels to file 
def save_label():
    global label_list
    for var,rect in zip(yolo_button_var_list, yolo_rect_list):
        if var.get():
            x1, y1, x2, y2 = yolo_canvas.coords(rect)
            x1 = max(min(x1, resolution), 0)
            y1 = max(min(y1, resolution), 0)
            x2 = max(min(x2, resolution), 0)
            y2 = max(min(y2, resolution), 0)
            label_list.append((x1, y1, x2, y2))

    if len(label_list) == 0:
        print('no label in' + img_names[img_idx])
        return

    f = open(revised_label_path + img_names[img_idx] + '.txt', 'w')
    for box in label_list:
        label = ['0', *xyxy2xywh(*box, dtype=str, scale=1/resolution)]
        f.write(' '.join(label) + '\n')
    f.close()
    print('Write %d'%len(label_list) + ' labels to ' + img_names[img_idx] + '.txt')

img_idx = -1
# show next image
def show_next():
    global yolo_button_list
    global yolo_button_var_list
    global yolo_rect_list

    global img_names
    global img_idx

    global img_file
    global yolo_img

    global gt_img
    global gt_img_file

    global label_list

    # clear canvas
    yolo_canvas.delete('all')
    gt_canvas.delete('all')

    # clear button
    for button in yolo_button_list:
        button.destroy()

    # clear lists
    yolo_button_list = []
    yolo_button_var_list = []
    yolo_rect_list = []
    label_list = []

    # get next img
    img_idx += 1
    if img_idx == len(img_names):
        exit()
    img_name = img_names[img_idx]

    lat = int(img_name.split('_')[0])

    # show progress on title
    window.title(' ' + img_name + '.png   %d/%d'%((done_work_num + img_idx), (done_work_num + total_work_num)))

    # read image & show image on two canvas
    img_file = tk.PhotoImage(file=(img_path + img_name + '.png'))
    yolo_img = yolo_canvas.create_image(0, 0, anchor='nw', image=img_file)

    gt_img_file = tk.PhotoImage(file=(gt_label_image_path + img_name + '.png'))
    gt_img = gt_canvas.create_image(0, 0, anchor='nw', image=gt_img_file)

    # read gt labels
    try:
        gt_label_file = open(gt_label_path + img_name + '.txt', 'r')
        gt_label_list = [xywh2xyxy(*line.split()[1:5], dtype=round, scale=resolution)  for line in gt_label_file.read().splitlines()]
        gt_label_file.close()
    except Exception as inst:
        print(inst)    
        gt_label_list = []

    # read robbins labels
    try:
        robbins_label_file = open(robbins_label_path + img_name + '.txt', 'r')
        robbins_label_list = [xywh2xyxy(*line.split()[1:5], dtype=round, scale=resolution)  for line in robbins_label_file.read().splitlines()]
        robbins_label_file.close()
    except Exception as inst:
        print(inst)    
        robbins_label_list = []

    # read yolo labels
    try:
        yolo_label_file = open(yolo_label_path + img_name + '.txt', 'r')
        yolo_label_list = [line.split(' ') for line in yolo_label_file.read().splitlines()]
        yolo_label_file.close()
        yolo_label_list.sort(key=(lambda label : -float(label[5])))
    except:
        yolo_label_list = []
    
    # show yolo labels
    for label in yolo_label_list:
        x, y, w, h = label[1:5]
        # h = float(h) * 0.9
        x1, y1, x2, y2 = xywh2xyxy(x, y, w, h, dtype=round, scale=resolution)
        try:
            conf = float(label[5][:5])
        except:
            conf = 1

        w_true = float(w) * cos(radians(lat))
        h_true = float(h)

        # if it's a partial crater, ignore it
        if (max(w_true, h_true) / min(w_true, h_true) > 2) or conf < conf_thresh:
            continue

        # find most relevant crater from ground truth dataset
        max_iou, max_iou_box = find_max_iou_box((x1, y1, x2, y2), gt_label_list)
        
        # if there is a crater, then select the average one
        if max_iou > iou_thresh:
            gt_label_list.remove(max_iou_box)
            label_list.append(average_two_box((x1, y1, x2, y2), max_iou_box))
            # label_list.append((x1, y1, x2, y2))
            continue

        # if in robbins dataset
        max_iou, max_iou_box = find_max_iou_box((x1, y1, x2, y2), robbins_label_list)
        if max_iou > iou_thresh:
            robbins_label_list.remove(max_iou_box)
            label_list.append((x1, y1, x2, y2))
            continue


        # if there is not a crater in gt dataset,
        # and the confidence is good,
        # add it to dataset directly
        if conf > conf_thresh_up:
            label_list.append((x1, y1, x2, y2))
            continue

        color = get_random_color()
        # create rect
        rect = yolo_canvas.create_rectangle(x1, y1, x2, y2, outline=color)
        yolo_rect_list.append(rect)

        # create button
        button_var = tk.IntVar(value=1)
        yolo_button_var_list.append(button_var)

        button = tk.Checkbutton(yolo_button_frame, text=conf, variable=button_var, font=font, bg=color, width=10, command=yolo_button_action)
        button.pack()
        yolo_button_list.append(button)

    print('detected and already in gt:', len(label_list))

    label_list += gt_label_list

    print('total not shown:', len(label_list))
    

    if len(yolo_rect_list) == 0:
        save_label()
        show_next()
    else:
        img_idx_stack.append(img_idx)

'''
    action function
'''
def keyboard_action(event):
    key = event.keysym
    if key == 'Return':
        save_label()
        show_next()
    elif key == '1':
        for button_var in yolo_button_var_list:
            button_var.set(1)
        yolo_button_action()
    elif key == '2':
        for button_var in yolo_button_var_list:
            button_var.set(0)
        yolo_button_action()
    elif key == 'bracketleft':
        global img_idx_stack
        global img_idx
        if len(img_idx_stack) >= 2:
            img_idx_stack.pop()
            img_idx = img_idx_stack.pop() - 1
            show_next()
    elif key == 'bracketright':
        show_next()
window.bind('<Key>', keyboard_action)


selected_box_idx = -1
# click left mouse to select
def select_box_by_mouse(event):
    global selected_box_idx
    if event.widget == yolo_canvas:
        global x_move_from
        global y_move_from
        x = event.x
        y = event.y
        x_move_from = x
        y_move_from = y
        print(x, y)
        global selected_box_idx
        candidate = -1
        candidate_area = resolution * resolution
        for i, rect in enumerate(yolo_rect_list):
            x0, y0, x1, y1 = yolo_canvas.coords(rect)
            area = (x1 - x0) * (y1 - y0)
            if x0 < x < x1 and y0 < y < y1 and area < candidate_area:
                candidate = i
                candidate_area = area

        selected_box_idx = candidate
        
window.bind('<Button-1>', select_box_by_mouse)

# drag and move a box
def on_drag(event):
    global selected_box_idx
    if event.widget == yolo_canvas and selected_box_idx >= 0:
        rect = yolo_rect_list[selected_box_idx]
        x0, y0, x1, y1 = yolo_canvas.coords(rect)
        w = x1 - x0
        h = y1 - y0
        # x = max(min(event.x, resolution), w)
        # y = max(min(event.y, resolution), h)
        x = event.x
        y = event.y
        yolo_canvas.coords(rect, x - w, y - h, x, y)
window.bind('<B1-Motion>', on_drag)


show_next()
window.mainloop()