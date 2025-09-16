
# EyeLock-Timelapse

**EyeLock-Timelapse** aligns faces with a focus on eyes in multiple images and creates smooth timelapse videos. Upload your selfies, and the app automatically fixes eye positions for a perfectly aligned video ready to edit.  

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/NeuralFalconYT/EyeLock-Timelapse/blob/main/colab.ipynb) <br>


## Demo
Don’t sue me, **Mark Zuckerberg**, for using your images for this demo ❤️ <br> <br>
**Original images:**  


![Images](https://github.com/user-attachments/assets/2552dba5-48b7-4603-a637-7eb6581ee023)

**After eye alignment**  

https://github.com/user-attachments/assets/d231728a-a9cd-4865-b234-cf78388eed68


**After crop in the editing app (eyes are fixed and properly aligned)**


https://github.com/user-attachments/assets/ceee680e-9940-470b-adc4-95ffad323886


---

## Features

- Aligns faces focusing on eyes.  
- Automatically crops and fixes eye positions.  
- Creates smooth timelapse videos from multiple selfies.  
- Optional Gradio-based UI for easy use.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/NeuralFalconYT/EyeLock-Timelapse.git
cd EyeLock-Timelapse
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

> Make sure you have **Python 3.9+** installed.

---

## Usage

### 1. Without Gradio UI

You can directly use the module in your Python script:

```python
from eye_lock import EyeLock_Timelapse

# Path to folder containing selfies
timelapse_video = EyeLock_Timelapse("./selfies")

print("Timelapse video saved at:", timelapse_video)
```

### 2. With Gradio UI

Launch the Gradio app for an interactive interface:

```bash
python app.py
```

Then upload your images, and the app will generate the timelapse video automatically.

**Screenshot of Gradio App:**

<img width="1432" height="768" alt="Gradio UI Screenshot" src="https://github.com/user-attachments/assets/4b16898f-26e0-4e4e-b855-f9db16296a5d" />

---

## Output

* The final video will be saved in the working directory (default format: `.mp4`).
* Faces are aligned based on eye positions for smooth transitions.






