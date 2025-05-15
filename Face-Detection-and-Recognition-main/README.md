#  <p align ="center" height="40px" width="40px"> Face Detection and Recognition System 🧑🔍 </p>

### <p align ="center"> Implemented using: </p>
<p align ="center">
<a href="https://www.python.org/" target="_blank" rel="noreferrer">   <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png" width="64" height="64" /></a> 
<a href="https://opencv.org/" target="_blank" rel="noreferrer">   <img src="https://opencv.org/wp-content/uploads/2022/05/logo.png" width="64" height="64" /></a> 
</p>

<br>

### <p align ="center"> Do remember to star ⭐ the repository if you like what you see!</p>
<p align="center">
  <img src="https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99" alt="Star Badge"/> 
  <a href="https://github.com/NadavIs56/Face-Detection-and-Recognition/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/NadavIs56/Face-Detection-and-Recognition"></a>
</p>

<br>

![explain](https://github.com/NadavIs56/Face-Detection-and-Recognition/assets/73107945/3afcfd39-6ab8-4f7d-b99b-ddcd5fbc54e6)

<br>

## Introduction 🌟

Welcome to a customizable face recognition system designed to identify individuals in photographs based on a user-populated database of facial images. This powerful tool harnesses Python and its potent libraries, such as `face_recognition` and `opencv`, offering a blend of accuracy and user-centric functionality. Tailor the database with your images and let the system pinpoint matches with ease.

<br>

## Features 🚀

- **Face Detection**: Utilizes Haar Cascade classifiers to detect faces within images. 🔎
- **Face Recognition**: Matches detected faces against a pre-established database to identify individuals. 👤
- **Annotation**: Labels recognized faces with rectangles and their corresponding names. 🏷️
- **Scalability**: Designed with future enhancements in mind, including video file processing. 📈
  
<br>

## Installation 💻

Ensure you have Python installed, and then set up the required libraries with the following commands:

```bash
pip install face_recognition opencv-python
```
Get the code by cloning this repository:
```bash
git clone https://github.com/your-github-username/face-recognition-system.git
```
  
<br>


## Usage 📘
1. Prepare a database directory containing named images of individuals.
2. Execute the script.
3. Select an image through the file dialog prompt.
4. Let the system work its magic, detecting, recognizing, and annotating faces, saving the output as result.jpg.

### Running the Script
Navigate to the script's directory and run:
```bash
python main.py
```
  
<br>


## Database Structure 🗂️
The database should meet the following criteria:

- Only image formats such as .png, .jpg, .jpeg, .tiff, .bmp, or .gif.
- Each image should display only one individual's face.
- Image filenames should correspond to the individual's name.
  
<br>


## Output 🖼️
The processed image will be stored as **result.jpg** in the project's root directory, complete with labeled rectangles around each recognized face.
  
<br>


## Contributions 👐
Your contributions are welcome! If you have suggestions for improvements, please open an issue to kick off the discussion.
  
<br>

## Future Updates 🔄

**Here's what's on the horizon for this face recognition system:**

- **Video Processing**: We plan to extend the system's capabilities to detect and recognize faces in video files, enhancing its applicability in various real-world scenarios.
- **Real-Time Recognition**: Implementing the ability to recognize faces in real-time through live video feeds.

**Stay tuned for these exciting enhancements that will make the system more powerful and versatile for all users!**

<br>

## Acknowledgments 👏
Props to Haar Cascades for the face detection capabilities.
Gratitude to the face_recognition library for simplifying facial recognition technology.
Kudos to opencv and matplotlib for their powerful image processing and visualization tools.

<br>

### <p align ="center"> Do remember to star ⭐ the repository if you like what you see!</p>

---


<div align="center">
  Made with ❤️ by <a href="https://github.com/NadavIs56">Nadav Ishai</a>
</div>
