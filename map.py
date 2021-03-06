import pandas as pd
import numpy as np
from tifffile import imread
from PIL import Image
import os
from tqdm import tqdm
from math import cos, radians
import argparse
from utils import *
import threading
import time

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='dataset')
parser.add_argument('--scale', type=float, default=1.0)
parser.add_argument('--inbox-threshold', type=float, default=0.5)
parser.add_argument('--no-label', action='store_true')
parser.add_argument('--lat', type=int, default=90)
parser.add_argument('--threads', type=int, default=6)
opt = parser.parse_args()

print(opt)

dataset_path = opt.dataset
inbox_threshold = opt.inbox_threshold
box_scale = opt.scale
no_label = opt.no_label
lat_threshold = opt.lat
n_thread = opt.threads

slash = os.sep
os.system('mkdir ' + dataset_path)
os.system('mkdir ' + dataset_path + slash + 'images')
if not no_label:
    os.system('mkdir ' + dataset_path + slash + 'labels')

# define pixel per degree
resolution = 592.747
round_resolution = int(round(resolution))
data = pd.read_csv('Robbinsv2.csv')
lat_data = data['LATITUDE_CIRCLE_IMAGE']
lon_data = data['LONGITUDE_CIRCLE_IMAGE']

image_folder_path = dataset_path + '/images/'.replace('/', os.sep)
label_folder_path = dataset_path + '/labels/'.replace('/', os.sep)



def slice_image(im_name):
    # read image to a ndarray
    im = imread(im_name)

    print('\nslicing ' + im_name)
    print('-' * 30)
    print('image_size ', im.shape)

    # get lat and lon base and range
    lat_base, lon_base = get_lat_lon_base(im_name)
    lat_range = int(im.shape[0] / resolution)
    lon_range = int(im.shape[1] / resolution)

    print('lat_range [%d, %d]'%(lat_base, lat_base + lat_range))
    print('lon_range [%d, %d]'%(lon_base, lon_base + lon_range))

    lat_base += lat_range
    # define indexes
    origin_xs = np.linspace(0, im.shape[0], lat_range + 1)[:-1]
    ys = np.linspace(0, im.shape[1], lon_range + 1)[:-1]

    def parallel_x(xs):
        # slice and store
        for i, x in enumerate(tqdm(xs, ncols=100)):
            lat = lat_base - i
            if abs(lat) > lat_threshold:
                continue
            for j, y in enumerate(ys):
                # image
                lon = lon_base + j
                file_name = str(lat) + '_' + str(lon)
                round_x = int(round(x))
                round_y = int(round(y))
                pillow_im = Image.fromarray(im[round_x : round_x + round_resolution, round_y : round_y + round_resolution])
                
                if no_label:
                    pillow_im.save(image_folder_path + file_name + '.png', 'PNG')
                    continue

                # label
                craters = data[(lat_data <= lat) & (lat_data > lat - 1) & (lon_data >= lon) & (lon_data < lon + 1)]
                buffer = ''
                for lat_crater, lon_crater, w, h, id in zip(craters['LATITUDE_ELLIPSE_IMAGE'], craters['LONGITUDE_ELLIPSE_IMAGE'], craters['DIAM_ELLIPSE_MAJOR_IMAGE'], craters['DIAM_ELLIPSE_MINOR_IMAGE'], craters['CRATER_ID']):
                    # calculate x and y position in a tile
                    x_ = lon_crater - lon
                    y_ = lat - lat_crater

                    # caculate w and h
                    w = w * 10 / round_resolution / cos(radians(lat)) * box_scale
                    h = h * 10 / round_resolution * box_scale

                    # deal with partial craters
                    x0, y0 = max(0, x_ - w / 2), max(0, y_ - h / 2)
                    x1, y1 = min(1, x_ + w / 2), min(1, y_ + h / 2)

                    area = w * h
                    area_inbox = (x1 - x0) * (y1 - y0)

                    if area_inbox / area > inbox_threshold:
                        x_ = (x0 + x1) / 2
                        y_ = (y0 + y1) / 2
                        w = x1 - x0
                        h = y1 - y0
                        buffer += ('0' + ' ' + str(x_) + ' ' + str(y_) + ' ' + str(w) + ' ' + str(h) + ' ' + id + '\n')
                    
                # if there is at least one crater in this tile, save this tile with image
                if len(buffer) > 0:
                    pillow_im.save(image_folder_path + file_name + '.png', 'PNG')
                    f = open(label_folder_path + file_name + '.txt', 'w')
                    f.write(buffer)
                    f.close()

    thread_list = []
    thread_args = list_to_thread_list(origin_xs, n_thread)
    for thread_arg in thread_args:
        thread = threading.Thread(target=parallel_x, args=(thread_arg, ))
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()

    time.sleep(1)
    print('\n'*n_thread)

# get the section lat and lon from filename
def get_lat_lon_base(file_name):
    latlon = file_name.split('_')[-2]
    if 'N' in latlon:
        code = latlon.split('N')
        lat = int(code[0])
        lon = int(code[1][:-1])
    else:
        code = latlon.split('S')
        lat = -int(code[0])
        lon = int(code[1][:-1])
    if lon >= 180:
        lon -= 360
    return lat, lon


raw_folder_path = 'raw_images/'
raw_ims = os.listdir(raw_folder_path)
for i, im_name in enumerate(raw_ims):
    print('--------%d/%d---------'%(i, len(raw_ims) - 1))
    slice_image(raw_folder_path + im_name)
    # os.system('rm -f %s'%(raw_folder_path + im_name))