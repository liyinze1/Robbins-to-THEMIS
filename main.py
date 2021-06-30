import pandas as pd
import numpy as np
from tifffile import imread
from PIL import Image
import os
from tqdm import tqdm

# define pixel per degree
resolution = 592.747
round_resolution = round(resolution)
data = pd.read_csv('RobbinsCraters_tab.csv')
lat_data = data['LATITUDE_CIRCLE_IMAGE']
lon_data = data['LONGITUDE_CIRCLE_IMAGE']

image_folder_path = 'crater_dataset/images/'
label_folder_path = 'crater_dataset/labels/'

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
    xs = np.linspace(0, im.shape[0], lat_range + 1)[:-1]
    ys = np.linspace(0, im.shape[1], lon_range + 1)[:-1]

    # slice and store
    for i, x in enumerate(tqdm(xs)):
        for j, y in enumerate(ys):
            # image
            lat = lat_base - i
            lon = lon_base + j
            file_name = str(lat) + '_' + str(lon)
            pillow_im = Image.fromarray(im[round(x) : round(x) + round_resolution, round(y) : round(y) + round_resolution])
            pillow_im.save(image_folder_path + file_name + '.png', 'PNG')
            
            # label
            f = open(label_folder_path + file_name + '.txt', 'w')
            craters = data[(lat_data <= lat) & (lat_data > lat - 1) & (lon_data >= lon) & (lon_data < lon + 1)]
            for lat_crater, lon_crater, w, h in zip(craters['LATITUDE_ELLIPSE_IMAGE'], craters['LONGITUDE_ELLIPSE_IMAGE'], craters['DIAM_ELLIPSE_MAJOR_IMAGE'], craters['DIAM_ELLIPSE_MINOR_IMAGE']):
                x_ = lon_crater - lon
                y_ = lat - lat_crater
                w = w * 10 / round_resolution
                h = h * 10 / round_resolution
                f.write('0' + ' ' + str(x_) + ' ' + str(y_) + ' ' + str(w) + ' ' + str(h) + '\n')
            f.close()

def get_lat_lon_base(file_name):
    code = file_name.split('_')[-2]
    lat = int(code[0 : 2])
    if code[2] == 'S':
        lat = -lat
    lon = int(code[3 : -1])
    if lon >= 180:
        lon -= 360
    return lat, lon

if __name__ == '__main__':
    raw_folder_path = 'raw_images/'
    raw_ims = os.listdir(raw_folder_path)
    for im_name in raw_ims:
        slice_image(raw_folder_path + im_name)