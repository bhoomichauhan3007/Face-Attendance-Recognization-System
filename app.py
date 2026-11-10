from flask import Flask, render_template, Response, jsonify
import cv2
import pickle
import os
import numpy as np
import time
from src.attendance import mark_attendance, get_attendance, get_today_count

app = Flask(__name__)

# ========== LOAD MODEL ==========
MODEL_PATH = "models/model.yml"
NAMES_PATH = "models/names.pkl"
CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'

face_detector = cv2.CascadeClassifier(CASCADE_PATH)
recognizer = None
names = {}

if hasattr(cv2, 'face') and os.path.exists(MODEL_PATH) and os.path.exists(NAMES_PATH):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_PATH)
    with open(NAMES_PATH, 'rb') as f:
        names = pickle.load(f)
    print(f"[OK] Model loaded. Names: {names}")
else:
    print("[ERROR] Model not found or cv2.face not available!")


def make_error_frame(msg):
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(frame, msg, (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    ret, buffer = cv2.imencode('.jpg', frame)
    return buffer.tobytes()


def generate_frames(lecture):
    camera = None

    for idx in [0, 1]:
        for backend in [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]:
            print(f"[CAMERA] Trying index={idx}, backend={backend}...")
            camera = cv2.VideoCapture(idx, backend)
            if camera.isOpened():
                ret, test = camera.read()
                if ret and test is not None:
                    print(f"[CAMERA] SUCCESS with index={idx}, backend={backend}")
                    break
                else:
                    camera.release()
                    camera = None
            else:
                camera = None
        if camera is not None:
            break

    if camera is None or not camera.isOpened():
        print("[CAMERA] FAILED to open any camera!")
        error_bytes = make_error_frame("Camera not found! Check connection.")
        while True:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + error_bytes + b'\r\n')
            time.sleep(1)
        return

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    fail_count = 0

    while True:
        success, frame = camera.read()

        if not success or frame is None:
            fail_count += 1
            if fail_count > 30:
                error_bytes = make_error_frame("Camera disconnected!")
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + error_bytes + b'\r\n')
                time.sleep(1)
                continue
            time.sleep(0.05)
            continue

        fail_count = 0

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=4, minSize=(40, 40)
        )

        for (x, y, w, h) in faces:
            color = (0, 0, 255)
            label = "Unknown"

            if recognizer is not None:
                face_roi = cv2.resize(gray[y:y+h, x:x+w], (100, 100))
                pred_id, confidence = recognizer.predict(face_roi)

                # Set threshold to 105 so it's relaxed enough to actually recognize registered users
                if confidence < 105:
                    pred_name = names.get(pred_id, "Unknown")
                    if pred_name != "Unknown":
                        label = f"{pred_name}"
                        color = (0, 255, 0)
                        mark_attendance(pred_name, lecture)
            else:
                label = "No Model"

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.rectangle(frame, (x, y-30), (x+w, y), color, -1)
            cv2.putText(frame, label, (x+5, y-8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    camera.release()


@app.route('/')
def home():
    return render_template("dashboard.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/start')
def start():
    return render_template("camera.html")

@app.route('/video_feed')
def video_feed():
    from flask import request
    lecture = request.args.get('lecture', 'Unknown')
    return Response(generate_frames(lecture),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/attendance')
def attendance_page():
    return render_template("attendance.html")

@app.route('/api/attendance')
def get_attendance_data():
    try:
        return jsonify(get_attendance())
    except:
        return jsonify([])

@app.route('/api/stats')
def get_stats():
    from flask import request
    lecture = request.args.get('lecture', None)
    try:
        return jsonify({"present": get_today_count(lecture)})
    except:
        return jsonify({"present": 0})

@app.route('/dataset')
def dataset_page():
    return render_template("dataset.html")

@app.route('/api/dataset')
def dataset_api():
    import base64
    from flask import send_from_directory
    data = []
    if os.path.exists("dataset"):
        for d in os.listdir("dataset"):
            p = os.path.join("dataset", d)
            if os.path.isdir(p):
                name = d.replace("_images", "").replace("_image", "").title()
                data.append({"name": name, "folder": d})
    return jsonify(data)

@app.route('/dataset_img/<folder>')
def dataset_img(folder):
    from flask import send_from_directory
    p = os.path.join("dataset", folder)
    if os.path.exists(p):
        imgs = [f for f in os.listdir(p) if f.endswith(('.jpg', '.png', '.jpeg'))]
        if imgs:
            return send_from_directory(p, imgs[0])
    return ""

if __name__ == "__main__":
    app.run(debug=True, threaded=True)