# face-recognition-project
Program allows you to control the cursor with moving your head
and blinking.  

The project was created by Ondřej Soukeník, Pavel Vaněk 
and Zdeňka Varmužová as the final project in Computer programming 2.


## Installation

Prerequisites: webcam, python 3, virtualenv and pip

Python dependencies: opencv-python, imutils, pyautogui, scipy

Create and activate virtual environment (for GNU/Linux):

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
pip install opencv-python pyautogui imutils scipy
```

Clone repository and run the project:

```
git clone https://github.com/ondrasouk/face-recognition-project
cd face-recognition-project
python main.py
```

## Control via keyboard
Q - Quit script  
R - New reference point  
E - Enable/disable mouse movements
