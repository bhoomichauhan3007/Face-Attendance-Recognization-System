# Face Recognition Attendance System

An AI-powered attendance management system that uses face detection and recognition to identify students and automate the attendance process. Built using Python, OpenCV, and Flask, the project provides a web-based interface to manage and view attendance records.

## Features

- **Face Detection:** Detects human faces using OpenCV.
- **Face Recognition:** Identifies registered students using their facial images.
- **Automated Attendance:** Records attendance based on recognized faces.
- **Web Dashboard:** Provides a simple and user-friendly interface.
- **Attendance Records:** Displays attendance information for registered students.
- **Real-Time Camera Support:** Uses a webcam for face detection and recognition.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OpenCV | Face detection and image processing |
| Flask | Web application and backend |
| HTML | Web page structure |
| CSS | User interface styling |
| CSV / Database | Attendance data storage |

## Project Structure

```text
Face-Recognition-Attendance-System/
│
├── dataset/                 # Student face images
├── models/                  # Trained recognition models
├── attendance/              # Attendance records
├── static/                  # CSS and static files
├── templates/               # HTML templates
│   ├── welcome.html
│   ├── dashboard.html
│   ├── camera.html
│   ├── success.html
│   └── attendance.html
│
├── src/                     # Source code
│   ├── encode_faces.py
│   ├── recognize.py
│   └── attendance.py
│
├── app.py                   # Flask application
├── haarcascade_frontalface_default.xml
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Face-Recognition-Attendance-System.git
```

### 2. Navigate to the Project Folder

```bash
cd Face-Recognition-Attendance-System
```

### 3. Install Required Libraries

```bash
pip install flask opencv-python numpy
```

### 4. Run the Application

```bash
python app.py
```

### 5. Open in Browser

Visit:

```text
http://127.0.0.1:5000
```

## How It Works

1. Student face images are collected and stored in the dataset.
2. The system uses OpenCV to detect faces through a webcam.
3. Detected faces are processed and compared with registered student data.
4. Once a student is recognized, their attendance can be recorded.
5. Attendance information can be viewed through the web dashboard.

## Future Improvements

- Improve recognition accuracy under different lighting conditions.
- Add student registration through the web interface.
- Integrate a database for attendance management.
- Generate daily and monthly attendance reports.
- Add authentication for administrators.
- Improve the user interface and dashboard analytics.

## Author

**Bhoomi Chauhan**

B.Tech Computer Science and Engineering

---

*This project is developed for educational purposes as an AI-based attendance management solution.*
