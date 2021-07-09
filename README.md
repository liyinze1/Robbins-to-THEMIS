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
* This script will download 30 .tif images to ./raw_images/
## 2. Slice THEMIS images and label craters based on Robbins dataset
```
python main.py
```
* Image folder: ./dataset/images/

* Label folder: ./dataset/labels/
## 3. Split dataset
```
python split.py
```
* Validation set folder: ./valid/

* Default Train : Valid = 8 : 2
## 4. Open the GUI tool for correct labels
```
python gui.py
```
* The gui will read images from ./dataset/images/ and read labels from ./dataset/labels/ if labels exist. 

* Then the revised labels will be in ./dataset/revised_labels/

