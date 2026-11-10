# Face Recognition Attendance System

An automated attendance management system built using **Python, OpenCV, Flask, and Face Recognition**. The system uses facial recognition to identify registered individuals and helps record their attendance digitally.

## Overview

The Face Recognition Attendance System aims to simplify the traditional attendance process by replacing manual attendance marking with an automated face recognition approach.

The application captures images through a camera, detects faces, recognizes registered individuals, and records attendance. It also provides a web-based interface for interacting with the system.

## Features

- **Face Detection:** Detects human faces using OpenCV.
- **Face Recognition:** Uses the Local Binary Patterns Histograms (LBPH) algorithm to recognize registered faces.
- **Automated Attendance:** Records attendance after successful face recognition.
- **Web Interface:** Provides a Flask-based interface for accessing different application pages.
- **Attendance Management:** Supports attendance-related operations.
- **Modular Structure:** Separates face recognition, attendance processing, utility functions, and interface components.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OpenCV | Image processing and face detection |
| LBPH | Face recognition |
| Flask | Backend web framework |
| HTML | Web page structure |
| CSS | User interface styling |
| NumPy | Numerical operations |

## Project Structure

```text
Face-Attendance-Recognization-System/
│
├── Dashboard/
│   ├── attendance_page.py
│   ├── camera_screen_page.py
│   ├── styles.py
│   ├── success_screen_page.py
│   └── welcome_page.py
│
├── src/
│   ├── attendance.py
│   ├── encode_faces.py
│   ├── recognize_faces.py
│   └── utils.py
│
├── templates/
│   ├── attendance.html
│   ├── camera.html
│   ├── dashboard.html
│   ├── dataset.html
│   ├── success.html
│   └── welcome.html
│
├── static/
│   └── style.css
│
├── assests/
│
├── app.py
├── optimize_dataset.py
├── README.md
└── test_model.py
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/bhoomichauhan3007/Face-Attendance-Recognization-System.git
```

### 2. Navigate to the Project Directory

```bash
cd Face-Attendance-Recognization-System
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Install Dependencies

Install the required Python libraries:

```bash
pip install flask opencv-contrib-python numpy pandas
```

If the project includes a `requirements.txt` file, use:

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
python app.py
```

Open the local URL displayed in the terminal in your web browser.

## How It Works

1. **Face Registration:** Images of individuals are collected and stored locally for recognition.
2. **Face Detection:** OpenCV detects faces from the camera input.
3. **Face Recognition:** The LBPH face recognizer compares detected faces with the trained recognition model.
4. **Attendance Processing:** When a registered face is recognized, the system processes the attendance entry.
5. **Attendance Record:** Attendance information is stored locally for further reference.

## Algorithms Used

### Haar Cascade
Used for detecting faces in images or camera frames.

### Local Binary Patterns Histograms (LBPH)
A face recognition algorithm that extracts facial patterns and compares them with trained face data to identify individuals.

## Privacy and Data Security

- Face datasets and trained models are stored locally.
- Attendance records and personal face images are not included in the public GitHub repository.
- Face images are biometric data and should only be collected and used with appropriate consent.

## Future Improvements

- Integration with a centralized database.
- Improved recognition accuracy under different lighting conditions.
- User authentication and role-based access.
- Attendance analytics and report generation.
- Cloud-based attendance management.

## Author

**Bhoomi Chauhan**

B.Tech Computer Science and Engineering

GitHub: [bhoomichauhan3007](https://github.com/bhoomichauhan3007)

---

⭐ If you find this project interesting, feel free to explore the repository!
