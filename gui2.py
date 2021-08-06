import os
import tkinter as tk
import os
import random

resolution = 593
dataset_path = 'combined_dataset/'
yolo_label_path = dataset_path + 'yolo_labels/'

conf_thresh = 0.5

slash = os.sep
dataset_path = dataset_path.replace('/', slash)
yolo_label_path = yolo_label_path.replace('/', slash)
os.system('mkdir %srevised_labels' % dataset_path)

# read images
try:
    f = open(dataset_path + '/loss_rank.txt', 'r')
    f.readline()
    img_names = [line.split(',')[0] for line in f.read().splitlines()]
    img_names = [img for img in img_names if img.split('.')[0][-1] not in ['h', 'v']]
    img_format = 'png'
    f.close()
except:
    img_names = [name[:-4] for name in os.listdir(dataset_path + 'images')]

# remove done work from to-do list
done_work_names = set([name[:-4] for name in os.listdir(dataset_path + 'revised_labels')])
img_names = [name for name in img_names if name not in done_work_names]

# number of done labels
done_work_num = len(done_work_names)
# number of total labels
total_work_num = len(os.listdir(dataset_path + 'labels'))

img_idx = -1

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
    code for GT canvas on the right
'''
# create a frame for GT image on the left
gt_img_frame = tk.Frame(window, padx=10, pady=10)
gt_img_frame.pack(side='left')

gt_canvas = tk.Canvas(gt_img_frame, bg='lightgray', height=resolution, width=resolution, borderwidth=0, highlightthickness=0)
gt_canvas.pack()

'''
    code for check button of GT
'''
# create a list of tick button on the left
gt_button_frame = tk.Frame(window, padx=10, pady=10)
gt_button_frame.pack(side='left')


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

def xyxy2xywh(x1, y1, x2, y2, dtype=float, scale=1):
    x1, y1, x2, y2 = float(x1) * scale, float(y1) * scale, float(x2) * scale, float(y2) * scale
    return dtype((x1 + x2) / 2), dtype((y1 + y2) / 2), dtype(abs(x2 - x1)), dtype(abs(y2 - y1))

def xywh2xyxy(x, y, w, h, dtype=float, scale=1):
    x, y, w, h = float(x) * scale, float(y) * scale, float(w) * scale, float(h) * scale
    return dtype(x - w / 2), dtype(y - h / 2), dtype(x + w / 2), dtype(y + h / 2)

'''
    def some list to contain rects and buttons
'''
yolo_button_list = []
yolo_rect_list = []
yolo_button_var_list = []

gt_button_list = []
gt_button_var_list = []
gt_rect_list = []
gt_id_list = []

def yolo_button_action():
    for i, button_var in enumerate(yolo_button_var_list):
        if button_var.get():
            yolo_canvas.itemconfigure(yolo_rect_list[i], state='normal')
        else:
            yolo_canvas.itemconfigure(yolo_rect_list[i], state='hidden')

def gt_button_action():
    for i, button_var in enumerate(gt_button_var_list):
        if button_var.get():
            gt_canvas.itemconfigure(gt_rect_list[i], state='normal')
        else:
            gt_canvas.itemconfigure(gt_rect_list[i], state='hidden')

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


def average_two_box(box1, box2):
    return [(n + m) / 2 for n, m in zip(box1, box2)]


# save labels to file 
def save_label():
    str_buffer = ''
    # process yolo boxes
    for i, button_var in enumerate(yolo_button_var_list):
        if button_var.get():
            yolo_rect = yolo_rect_list[i]
            box1 = yolo_canvas.coords(yolo_rect)
            box1_id = ''
            for gt_id, gt_rect in zip(gt_id_list, gt_rect_list):
                box2 = gt_canvas.coords(gt_rect)
                print(iou(box1, box2))
                if iou(box1, box2) > 0.5:
                    # they are the same box
                    box1_id = gt_id
                    
                    if gt_canvas.itemcget(gt_rect, 'state') == 'normal':
                        # if two boxes are both selected
                        box1 = average_two_box(box1, box2)

                    # remove this box from ground truth list
                    gt_rect_list.remove(gt_rect)
                    gt_id_list.remove(gt_id)
                    break
            
            x, y, w, h = xyxy2xywh(*box1, dtype=str, scale=1/resolution)
            str_buffer += ' '.join([x, y, w, h, box1_id])
            str_buffer += '\n'

    # process gt boxes
    for gt_id, gt_rect in zip(gt_id_list, gt_rect_list):
        if gt_canvas.itemcget(gt_rect, 'state') == 'normal':
            box2 = gt_canvas.coords(gt_rect)
            x, y, w, h = xyxy2xywh(*box2, dtype=str, scale=1/resolution)
            str_buffer += ' '.join([x, y, w, h, gt_id])
            str_buffer += '\n'

    f = open(dataset_path + 'revised_labels/' + img_names[img_idx] + '.txt', 'w')
    f.write(str_buffer)
    f.close()
    print('label: ' + img_names[img_idx] + '.txt has been saved')


# show next image
def show_next():
    global yolo_button_list
    global yolo_button_var_list
    global yolo_rect_list

    global gt_button_list
    global gt_button_var_list
    global gt_rect_list
    global gt_id_list

    global img_names
    global img_idx

    global img_file
    global gt_img
    global yolo_img

    # clear canvas
    yolo_canvas.delete('all')
    gt_canvas.delete('all')

    # clear button
    for button in yolo_button_list + gt_button_list:
        button.destroy()

    # clear lists
    yolo_button_list = []
    yolo_button_var_list = []
    yolo_rect_list = []

    gt_button_list = []
    gt_button_var_list = []
    gt_rect_list = []
    gt_id_list = []

    # get next img
    img_idx += 1
    if img_idx == len(img_names):
        exit()
    img_name = img_names[img_idx]

    # show progress on title
    window.title('No.' + str(done_work_num + img_idx) + ' ' + img_name + '.png------%.2f%%'%((done_work_num + img_idx) / total_work_num * 100))

    # read image & show image on two canvas
    img_file = tk.PhotoImage(file=(dataset_path + 'images/' + img_name + '.png'))
    yolo_img = yolo_canvas.create_image(0, 0, anchor='nw', image=img_file)
    gt_img = gt_canvas.create_image(0, 0, anchor='nw', image=img_file)

    # read yolo labels
    try:
        yolo_label_file = open(yolo_label_path + img_name + '.txt', 'r')
        yolo_label_list = [line.split(' ') for line in yolo_label_file.read().splitlines()]
        yolo_label_file.close()
        # sort boxes, from top to bottom
        yolo_label_list.sort(key=(lambda label : float(label[2])))
    except:
        yolo_label_list = []
    
    # show yolo labels
    for label in yolo_label_list:
        x1, y1, x2, y2 = xywh2xyxy(*label[1:5], dtype=round, scale=resolution)
        try:
            conf = label[5]
        except:
            conf = '1.0'
        if float(conf) < conf_thresh:
            continue
        if len(conf) > 3:
            conf = conf[:3]
        color = get_random_color()

        # create rect
        rect = yolo_canvas.create_rectangle(x1, y1, x2, y2, outline=color)
        yolo_rect_list.append(rect)

        # create button
        button_var = tk.IntVar(value=1)
        yolo_button_var_list.append(button_var)

        button = tk.Checkbutton(yolo_button_frame, text=conf, variable=button_var, font=font, bg=color, width=5, command=yolo_button_action)
        button.pack()
        yolo_button_list.append(button)


    # read gt labels
    try:
        gt_label_file = open(dataset_path + '/labels/' + img_name + '.txt', 'r')
        gt_label_list = [line.split(' ') for line in gt_label_file.read().splitlines()]
        gt_label_file.close()
        # sort boxes, from top to bottom
        gt_label_list.sort(key=(lambda label : float(label[2])))
    except:
        gt_label_list = []

    # show gt labels
    for label in gt_label_list:
        x1, y1, x2, y2 = xywh2xyxy(*label[1:5], dtype=round, scale=resolution)
        try:
            id = label[5]
        except:
            id = ''
        gt_id_list.append(id)
        color = get_random_color()

        # create rect
        rect = gt_canvas.create_rectangle(x1, y1, x2, y2, outline=color)
        gt_rect_list.append(rect)

        # create button
        button_var = tk.IntVar(value=1)
        gt_button_var_list.append(button_var)

        button = tk.Checkbutton(gt_button_frame, text=id, variable=button_var, font=font, bg=color, width=12, command=gt_button_action)
        button.pack()
        gt_button_list.append(button)

show_next()

'''
    here are some action function
'''
def keyboard_action(event):
    key = event.keysym
    print(key)
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
    elif key == '3':
        for button_var in gt_button_var_list:
            button_var.set(1)
        gt_button_action()
    elif key == '4':
        for button_var in gt_button_var_list:
            button_var.set(0)
        gt_button_action()
    elif key == 'bracketleft':
        global img_idx
        if img_idx > 0:
            img_idx -= 2
            show_next()
    elif key == 'bracketright':
        show_next()
    elif key == 'F1':
        hint_window = tk.Tk()
        hint_window.title('help')
        hint =  'Press 1/2 to select/deselect all yolo labels\n' +\
                'Press 3/4 to select/deselect all gt labels\n'
        tk.Label(hint_window, text=hint, font=font).pack()
        hint_window.mainloop()
window.bind('<Key>', keyboard_action)




window.mainloop()