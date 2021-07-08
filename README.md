# Robbins-to-THEMIS

## 0. Setup
```
pip install -r requirements.txt
```
## 1. Download THEMIS dataset
```
python download.py
```
## 2. Slice THEMIS images and label craters based on Robbins dataset
```
python main.py
```
## 3. Split dataset
* Default Train : Valid = 8 : 2
```
python split.py
```
## 4. Open the tool for correct labels
```
python gui.py
```
