import tkinter as tk
import os
import random
import threading
import time

# define file path
dataset_path = 'dataset/'

# create dir
os.system('mkdir ' + dataset_path + 'revised_labels/')

# read images
img_names = [name[:-4] for name in os.listdir(dataset_path + 'images/')]
# remove done work from to-do list
done_work_names = set([name[:-4] for name in os.listdir(dataset_path + 'revised_labels/')])
img_names = [name for name in img_names if name not in done_work_names]

resolution = 593
color_list = []
rect_list = []
radio_list = []
selected_box_idx = 0

move_keyset = {'w', 'a', 's', 'd', 'W', 'A', 'S', 'D'}
adjust_keyset = {'Up', 'Down', 'Left', 'Right'}

big_move = 5
small_move = 1

font = ('Courier', 15)

# create window
window = tk.Tk()
window.title('Let\'s correct lables!')
window.geometry('1000x650')


'''
    code for canvas on the left
'''
# create a frame for image on the left
img_frame = tk.Frame(window, padx=10)
img_frame.pack(side='left')

name_label = tk.Label(img_frame, font=font, width=15)
name_label.pack()

canvas = tk.Canvas(img_frame, bg='lightgray', height=resolution, width=resolution, borderwidth=0, highlightthickness=0)
canvas.pack()


'''
    Code for the list on the right
'''
# get the value of radio button
def radio_select():
    global selected_box_idx
    global radio_idx
    selected_box_idx = int(radio_idx.get())
    flash_selected_rect()

# colors
def get_random_color():
    global color_list
    R = G = B = 0
    # avoid gray color
    while max(R, G, B) - min(R, G, B) < 50:
        R = random.randint(0,255)
        G = random.randint(0,255)
        B = random.randint(0,255)
    color = '#' + '%02x'%R + '%02x'%G + '%02x'%B
    color_list.append(color)
    return color

# flash the selected box
def flash_thread():
    rect = rect_list[selected_box_idx]
    color = color_list[selected_box_idx]
    for i in range(2):
        time.sleep(0.1)
        canvas.itemconfig(rect, outline='#FFFFFF')
        time.sleep(0.1)
        canvas.itemconfig(rect, outline=color)
def flash_selected_rect():
    threading.Thread(target=flash_thread).start()

# save boxes to txt file
def save_labels():
    # save last image and label to 'revised_data/'
    if img_idx < 0:
        return
    global rect_list
    buffer = ''
    for rect in rect_list:
        x0, y0, x1, y1 = canvas.coords(rect)
        x = (x0 + x1) / 2 / resolution
        y = (y0 + y1) / 2 / resolution
        w = (x1 - x0) / resolution
        h = (y1 - y0) / resolution
        buffer += ' '.join(['0', str(x), str(y), str(w), str(h)])
        buffer += '\n'
    f = open(dataset_path + 'revised_labels/' + img_names[img_idx] + '.txt', 'w')
    f.write(buffer)
    f.close()
    print('label: ' + img_names[img_idx] + '.txt has been saved')

img_idx = -1
# show next image
def show_next():

    global rect_list
    global radio_list
    global radio_idx
    global img_idx
    global img
    global img_file
    global selected_box_idx
    global color_list

    img_idx += 1
    if img_idx == len(img_names):
        exit()
    img_name = img_names[img_idx]

    # clear canvas
    canvas.delete('all')
    name_label.config(text=str(img_idx) + '. ' + img_name)

    # display images
    img_file = tk.PhotoImage(file=(dataset_path + 'images/' + img_name + '.png'))
    img = canvas.create_image(0, 0, anchor='nw', image=img_file)

    # deselect
    selected_box_idx = -1

    # read labels
    try:
        label_file = open(dataset_path + 'labels/' + img_name + '.txt', 'r')
        label_list = [[float(item) for item in line.split(' ')] for i, line in enumerate(label_file.read().splitlines())]
        label_file.close()
    except:
        label_list = []
    # delete radiobuttons of last image
    radio_idx = tk.StringVar()
    for radio_button in radio_list:
        radio_button.forget()
    radio_list = []
    rect_list = []

    # delete color list
    color_list = []

    # draw rectangles
    for i, label in enumerate(label_list):
        x, y, w, h = label[1:]
        x *= resolution
        y *= resolution
        w *= resolution
        h *= resolution
        # get a color
        color = get_random_color()
        # create rectangles
        rect = canvas.create_rectangle(x - w / 2, y - h / 2, x + w / 2, y + h / 2, outline=color)
        rect_list.append(rect)
        # create radio buttons
        radio_button = tk.Radiobutton(radio_frame, text='Box ' + str(i), variable=radio_idx, value=i, command=radio_select, font=font, bg=color, width=8)
        radio_button.pack()
        radio_list.append(radio_button)
        
# create a image for labels and buttons on the right
list_frame = tk.Frame(window, padx=10, pady=10)
list_frame.pack(side='left')

hint = 'Click MouseLeft to select box\n' + \
       'Hold Shift+MouseLeft or MouseRight\nto draw a new box\n' + \
       'Press BackSpace to delete selected box\n' + \
       'Press Space to select next box\n' + \
       'Press w, a, s, d to move %d pixel\n'%small_move + \
       'Press W, A, S, D to move %d pixel\n'%big_move + \
       'Press ↔️ or ↕️ to adjust box\n' + \
       'Press Enter to save and show next image\n' + \
       'Press Esc to go back to last image\n'
hint_label = tk.Label(list_frame, text=hint, font=font)
hint_label.pack()

radio_frame = tk.Frame(list_frame)
radio_frame.pack()
radio_idx = tk.StringVar()


'''
    code for mouse and keyboard actions
'''  
# action for keyboard  
def keypress(event):
    key = event.keysym
    print(key)
    global selected_box_idx
    global move_keyset
    global rect_list
    global radio_list
    global radio_idx
    if key in move_keyset:
        if selected_box_idx == -1:
            return
        x = 0
        y = 0
        if key == 'a': x = -small_move 
        elif key == 'd': x = small_move
        elif key == 'w': y = -small_move
        elif key == 's': y = small_move
        elif key == 'A': x = -big_move
        elif key == 'D': x = big_move
        elif key == 'W': y = -big_move
        elif key == 'S': y = big_move
        x0, y0, x1, y1 = canvas.coords(rect_list[selected_box_idx])
        if x0 + x >= 0 and x1 + x <= resolution and y0 + y >= 0 and y1 + y <= resolution:
            canvas.move(rect_list[selected_box_idx], x, y)
    elif key in adjust_keyset:
        if selected_box_idx == -1:
            return
        rect = rect_list[selected_box_idx]
        x0, y0, x1, y1 = canvas.coords(rect)
        if key == 'Up': y1 = max(0, y1 - 1)
        elif key == 'Down': y1 = min(y1 + 1, resolution)
        elif key == 'Left': x1 = max(0, x1 - 1)
        elif key == 'Right': x1 = min(x1 + 1, resolution)
        canvas.coords(rect, x0, y0, x1, y1)
    elif key == 'Return':
        save_labels()
        show_next()
    elif key == 'Escape':
        global img_idx
        if img_idx > 0:
            img_idx -= 2
            show_next()
    elif key == 'space':
        selected_box_idx += 1
        selected_box_idx %= len(rect_list)
        radio_list[selected_box_idx].select()
        flash_selected_rect()
    elif key == 'BackSpace':
        print('here')
        # delete rectangle
        rect = rect_list[selected_box_idx]
        canvas.delete(rect)
        rect_list.remove(rect)
        # delete color
        del(color_list[selected_box_idx])
        # delete radio button
        for radio in radio_list:
            radio.forget()
        radio_list = []
        radio_idx.set('')
        for i, rect in enumerate(rect_list):
            radio_button = tk.Radiobutton(radio_frame, text='Box ' + str(i), variable=radio_idx, value=i, command=radio_select, font=font, bg=color_list[i], width=8)
            radio_button.pack()
            radio_list.append(radio_button)
        selected_box_idx = -1
    elif key == 'p':
        print(selected_box_idx)
        print('select box coords: ', canvas.coords(rect_list[selected_box_idx]))
window.bind('<Key>', keypress)

# action for mouse click
def select_box_by_mouse(event):
    if event.widget == canvas:
        x = event.x
        y = event.y
        print(x, y)
        global selected_box_idx
        candidate = -1
        candidate_area = resolution * resolution
        for i, rect in enumerate(rect_list):
            x0, y0, x1, y1 = canvas.coords(rect)
            area = (x1 - x0) * (y1 - y0)
            if x0 < x < x1 and y0 < y < y1 and area < candidate_area:
                candidate = i
                candidate_area = area
        if candidate == -1:
            radio_list[selected_box_idx].deselect()
            selected_box_idx = -1
        else:
            selected_box_idx = candidate
            radio_list[selected_box_idx].select()
            flash_selected_rect()
window.bind('<Button-1>', select_box_by_mouse)


x_start = 0
y_start = 0
# action for drag and drop
def on_click(event):
    if event.widget == canvas:
        global x_start
        global y_start
        global selected_box_idx
        global radio_list
        x_start = max(min(resolution, event.x), 0)
        y_start = max(min(resolution, event.y), 0)
        # create rectangle
        color = get_random_color()
        rect = canvas.create_rectangle(x_start, y_start, x_start, y_start, outline=color)
        # index
        i = len(rect_list)
        selected_box_idx = i
        rect_list.append(rect)
        # create new radio button
        radio_button = tk.Radiobutton(radio_frame, text='Box ' + str(i), variable=radio_idx, value=i, command=radio_select, font=font, bg=color, width=8)
        radio_button.pack()
        radio_list.append(radio_button)
        radio_button.select()

window.bind('<Shift-Button-1>', on_click)
window.bind('<Button-3>', on_click)

def on_move(event):
    if event.widget == canvas:
        x = max(min(resolution, event.x), 0)
        y = max(min(resolution, event.y), 0)
        canvas.coords(rect_list[selected_box_idx], x_start, y_start, x, y)
window.bind('<Shift-B1-Motion>', on_move)
window.bind('<B3-Motion>', on_move)

window.mainloop()
