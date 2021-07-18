import tkinter as tk
import os
import random
import threading
import time
import platform

crater_id_to_file = True

# define file path
if platform.system().lower() == 'windows':
    dataset_path = 'dataset\\'
    mv_cmd = 'move'
else:
    dataset_path = 'dataset/'
    mv_cmd = 'mv'

# create dir
os.system('mkdir ' + dataset_path + 'revised_labels')
os.system('mkdir ' + dataset_path + 'deleted_images')

# read images
img_names = [name[:-4] for name in os.listdir(dataset_path + 'images')]
# remove done work from to-do list
done_work_names = set([name[:-4] for name in os.listdir(dataset_path + 'revised_labels')])
img_names = [name for name in img_names if name not in done_work_names]

# number of done labels
done_work_num = len(done_work_names) + len(os.listdir(dataset_path + 'deleted_images'))
# number of total labels
total_work_num = len(os.listdir(dataset_path + 'labels'))

box_scale = 1.1
resolution = 593
color_list = []
rect_list = []
radio_list = []
crater_ids = []
selected_box_idx = 0

move_keyset = {'w', 'a', 's', 'd', 'W', 'A', 'S', 'D'}
adjust_keyset = {'Up', 'Down', 'Left', 'Right'}

big_move = 5
small_move = 1

font = ('Courier', 15)

rows_per_col = 10

# create window
window = tk.Tk()
window.title('Let\'s correct lables!')


'''
    code for canvas on the left
'''
# create a frame for image on the left
img_frame = tk.Frame(window, padx=10, pady=10)
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
    while max(R, G, B) - min(R, G, B) < 100:
        R = random.randint(60,255)
        G = random.randint(60,255)
        B = random.randint(60,255)
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
    global crater_ids
    buffer = ''
    for i, rect in enumerate(rect_list):
        x0, y0, x1, y1 = canvas.coords(rect)
        x = (x0 + x1) / 2 / resolution
        y = (y0 + y1) / 2 / resolution
        w = (x1 - x0) / resolution
        h = (y1 - y0) / resolution
        id = crater_ids[i]
        if crater_id_to_file:
            buffer += ' '.join(['0', str(x), str(y), str(w), str(h), id])
        else:
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
    global crater_ids

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
        label_list = [line.split(' ') for line in label_file.read().splitlines()]
        label_file.close()
        # sort boxes, from top to bottom
        label_list.sort(key=(lambda label : label[2]))
    except:
        label_list = []
    # delete radiobuttons of last image
    radio_idx = tk.StringVar()
    for radio_button in radio_list:
        radio_button.destroy()
    radio_list = []
    rect_list = []

    # delete color list
    color_list = []

    # delete crater ids of last image
    crater_ids = []

    # show work progress
    window.title('Let\'s correct lables!---%.2f%%'%((done_work_num + img_idx) / total_work_num * 100))

    # draw rectangles
    for i, label in enumerate(label_list):
        x = resolution * float(label[1])
        y = resolution * float(label[2])
        w = resolution * float(label[3]) * box_scale
        h = resolution * float(label[4]) * box_scale
        try:
            id = label[5]
        except:
            id = ''

        crater_ids.append(id)
        # get a color
        color = get_random_color()
        # create rectangles
        rect = canvas.create_rectangle(x - w / 2, y - h / 2, x + w / 2, y + h / 2, outline=color)
        rect_list.append(rect)
        # create radio buttons
        radio_button = tk.Radiobutton(radio_frame, text=id, variable=radio_idx, value=i, command=radio_select, font=font, bg=color, width=12)
        # radio_button.pack()
        radio_button.grid(row=i%rows_per_col, column=i//rows_per_col)
        radio_list.append(radio_button)
        
# create a image for labels and buttons on the right
list_frame = tk.Frame(window, padx=10, pady=10)
list_frame.pack(side='left')

hint = \
        '1. Select a box: click box or press space\t\n' + \
        '2. Move a box: leftmouse drag and drop or\t\n' + \
        'press w, a, s, d to move %d pixel\n'%small_move + \
        'press W, A, S, D to move %d pixel\n'%big_move + \
        '3. Adjust a box: press ⬆️⬇️⬅️➡️\t\t\t\n' + \
        '4. Create a box: shift+leftmouse or rightmouse\t\n' + \
        '5. Delete a box: press shift+backspace\delete\t\n' + \
        '6. Save and show next image: return or enter\t\n' + \
        '7. Last or next image without save: [ or ]\t\n' + \
        '8. Delete this image from dataset: shift+esc\t\n'
hint_label = tk.Label(list_frame, text=hint, font=font)
hint_label.pack()

radio_frame = tk.Frame(list_frame)
radio_frame.pack()
# radio button var
radio_idx = tk.StringVar()

show_next()

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
    global crater_ids
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
    elif key == 'bracketleft':
        global img_idx
        if img_idx > 0:
            img_idx -= 2
            show_next()
    elif key == 'bracketright':
        show_next()
    elif key == 'space':
        selected_box_idx += 1
        selected_box_idx %= len(rect_list)
        radio_list[selected_box_idx].select()
        flash_selected_rect()        
    elif key == 'p':
        print(selected_box_idx)
        print('select box coords: ', canvas.coords(rect_list[selected_box_idx]))
window.bind('<Key>', keypress)

# delete a box
def delete_box_by_keys(event):
    global selected_box_idx
    global radio_list
    global crater_ids
    global color_list
    global radio_idx
    if selected_box_idx == -1:
        return
    # delete rectangle
    rect = rect_list[selected_box_idx]
    canvas.delete(rect)
    rect_list.remove(rect)
    # delete color
    del(color_list[selected_box_idx])
    # delete crater id
    del(crater_ids[selected_box_idx])
    # delete radio button
    for radio in radio_list:
        radio.destroy()
    radio_list = []
    radio_idx.set('')
    for i, rect in enumerate(rect_list):
        radio_button = tk.Radiobutton(radio_frame, text=crater_ids[i], variable=radio_idx, value=i, command=radio_select, font=font, bg=color_list[i], width=12)
        # radio_button.pack(
        radio_button.grid(row=i%rows_per_col, column=i//rows_per_col)
        radio_list.append(radio_button)
    selected_box_idx = -1
window.bind('<Shift-BackSpace>', delete_box_by_keys)
window.bind('<Shift-Delete>', delete_box_by_keys)

# delete image
def delete_image_by_keys(event):
    global img_names
    global img_idx
    os.system(mv_cmd + ' ' + dataset_path + 'images/' + img_names[img_idx] + '.png ' + dataset_path + 'deleted_images')
    print('move ' + img_names[img_idx] + ' to /deleted_images/')
    show_next()
window.bind('<Shift-Escape>', delete_image_by_keys)

# click left mouse to select
def select_box_by_mouse(event):
    if event.widget == canvas:
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

# drag and move a box
def on_drag(event):
    if event.widget == canvas and selected_box_idx >= 0:
        rect = rect_list[selected_box_idx]
        x0, y0, x1, y1 = canvas.coords(rect)
        w = x1 - x0
        h = y1 - y0
        x = max(min(event.x, resolution), w)
        y = max(min(event.y, resolution), h)
        canvas.coords(rect, x - w, y - h, x, y)
window.bind('<B1-Motion>', on_drag)


x_start = 0
y_start = 0
# click right to mouse to create a box
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
        crater_ids.append('')
        # create new radio button
        radio_button = tk.Radiobutton(radio_frame, text='', variable=radio_idx, value=i, command=radio_select, font=font, bg=color, width=12)
        # radio_button.pack()
        radio_button.grid(row=i%rows_per_col, column=i//rows_per_col)
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
