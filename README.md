# face-recognition-project

## Instalation

Prerequisities: webcam, python 3, virtualenv and pip

Python depencies: opencv-python, face-recognition, pyautogui

Create and activate virtual enviroment (for GNU/Linux):

```
virtualenv ./env
source env/bin/activate 
```

For Windows:

```
python3 -m venv ./env
env\Scripts\activate.bat
```

Install pip packages:

```
pip install opencv-python face-recognition pyautogui
```

Clone repository and run the project:

```
git clone https://github.com/ondrasouk/face-recognition-project
cd face-recognition-project
python main.py
```
Module used for EAR  sensing is included in:
```
imutils_master
```
This new file are pre learned data for analysing face landmarks:
```
shape_predictor_68_face_landmarks.dat
```