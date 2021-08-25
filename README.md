# Robbins-to-THEMIS

## 0. Setup
For windows, please download [wget](https://eternallybored.org/misc/wget/) and copy wget.ext to C:\Windows\System32
```
pip install -r requirements.txt
```
## 1. Download THEMIS dataset
```
python download.py
```
Argument:
* -n the number of images to download, 1 < n <= 30. If you don't want any images > 65°, please input n <= 16
* This script will download 30 .tif images to ./raw_images/
## 2. Slice THEMIS images and label craters based on Robbins dataset
```
python map.py
```
Arguments:
* --dataset the/path/to/the/output/folder, default = ./dataset
* --scale scale for the the width and height, default = 1.0
* --inbox-threshold threshold for labelling those partial craters, default = 0.5
* --no-label just generate tiles without any label
## 3. Open the GUI tool for correct labels
```
python gui.py
```
* The gui will read images from ./dataset/images/ and read labels from ./dataset/labels/ if labels exist. 

* Then the revised labels will be in ./dataset/revised_labels/

## 4. Data augmentation
```
python aug.py
```
Arguments:
* --dataset the/path/to/the/dataset/folder, default = ./dataset
* --clean de-augmentation
* --no-label don't augment labels
* --no-image don't augment images
* --id augment labels with crater id
## 5. Split dataset
```
python split.py
```
Arguments:
* --dataset the/path/to/the/dataset/folder, default = ./dataset
* --valid validation set ratio, default = 0.2
* --test test set ratio, default = 0.0
* --prefix prefix path of image files, default = ../Robbins-to-THEMIS/dataset
Output:
* train.txt
* valid.txt if valid ratio > 0
* test.txt if test ratio > 0
* all.txt contains all the files