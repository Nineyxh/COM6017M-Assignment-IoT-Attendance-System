import cv2
import face_recognition
import os
import numpy as np
import serial
import time
import csv
from datetime import datetime

# --- SYSTEM CONFIGURATION ---
SERIAL_PORT = '/dev/ttyACM0'  # Check via 'ls /dev/tty*'
BAUD_RATE = 9600
KNOWN_FACES_DIR = "known_faces"
LOG_FILE = "attendance_log.csv"
TOLERANCE = 0.5  # Lower is stricter

# --- 1. SETUP M2M CONNECTION ---
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    ser.flush()
    print(f"[System] Connected to Arduino at {SERIAL_PORT}")
except Exception as e:
    print(f"[Error] Serial Connection Failed: {e}")
    exit()

# --- 2. LOAD EDGE AI MODEL ---
known_face_encodings = []
known_face_names = []

if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

print("[System] Loading biometric database...")
for filename in os.listdir(KNOWN_FACES_DIR):
    if filename.endswith((".jpg", ".png")):
        # Load image into dlib
        image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{filename}")
        # Generate 128D face encoding
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_face_encodings.append(encodings[0])
            name = os.path.splitext(filename)[0]
            known_face_names.append(name)
            print(f"  > Loaded Identity: {name}")

print("[System] Ready. Waiting for M2M trigger signal...")

# --- 3. MAIN EVENT LOOP ---
while True:
    try:
        if ser.in_waiting > 0:
            # Read signal from Arduino
            line = ser.readline().decode('utf-8').strip()
            
            if line == "CHECKIN":
                print("\n[Event] Trigger Received. Activating Computer Vision...")
                
                # Wake up camera (V4L2 backend for RPi)
                video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
                video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                
                start_time = time.time()
                detected_name = "Unknown"
                
                # Keep camera open for 10 seconds
                while (time.time() - start_time) < 10:
                    ret, frame = video_capture.read()
                    if not ret:
                        break
                    
                    # Resize for faster inference (0.25x scale)
                    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
                    
                    # Detect faces
                    face_locations = face_recognition.face_locations(rgb_small_frame)
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                    face_names = []
                    for face_encoding in face_encodings:
                        # Compare with database
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, TOLERANCE)
                        name = "Unknown"
                        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                        
                        if len(face_distances) > 0:
                            best_match_index = face_distances.argmin()
                            if matches[best_match_index]:
                                name = known_face_names[best_match_index]
                                if name != "Unknown":
                                    detected_name = name
                        face_names.append(name)

                    # Draw bounding boxes (GUI)
                    for (top, right, bottom, left), name in zip(face_locations, face_names):
                        top *= 4; right *= 4; bottom *= 4; left *= 4
                        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                        cv2.rectangle(frame, (left, top), (right, bottom), color, 3)
                        cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
                    
                    cv2.imshow('IoT Attendance System', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                # Cleanup
                video_capture.release()
                cv2.destroyAllWindows()
                
                # --- 4. DATA LOGGING ---
                if detected_name != "Unknown":
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open(LOG_FILE, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([timestamp, detected_name, "Authorized"])
                    print(f"[Success] Attendance logged for: {detected_name}")
                else:
                    print("[Warning] User not recognized. Access Denied.")
                
                print("[System] Waiting for next user...")

    except KeyboardInterrupt:
        print("[System] Shutting down.")
        break
    except Exception as e:
        print(f"[Error] {e}")