# COM6017M-Assignment-IoT-Attendance-System
The source code portion of COM6017M
## 1.Project Overview
This project is a secure, **offline-first** biometric attendance system designed to address hygiene concerns and attendance fraud in post-pandemic environments. 

The system integrates **Machine-to-Machine (M2M)** communication and **Edge AI** technology. It uses an Arduino node for physical event triggering and a Raspberry Pi Edge Gateway for local facial recognition inference. A custom Web Dashboard provides real-time data analytics via WiFi.

## 2. Key Features
- **Edge AI Inference**: Runs ResNet-34 deep learning models locally on Raspberry Pi using `dlib` and `face_recognition`. No cloud APIs are used, ensuring 100% data privacy.
- **M2M Communication**: Utilizes Wired Serial (UART) protocol between Arduino and Raspberry Pi for zero-latency triggering and maximum security against wireless interference.
- **Real-time Analytics**: Hosts a local Flask Web Server to display attendance logs on mobile devices via a responsive dashboard.
- **Event-Driven Architecture**: The camera and AI pipeline are only activated upon physical button press, optimizing power consumption.

## 3. Hardware Requirements
1.  **Edge Gateway**: Raspberry Pi 4 Model B (4GB RAM recommended).
2.  **Sensor Node**: Arduino Uno R4 WiFi (or generic Arduino Uno).
3.  **Vision Sensor**: Standard USB Webcam (e.g., Logitech C270).
4.  **Input**: Tactile Push Button (4-pin).
5.  **Connectivity**: USB Type-A to Type-C cable (for Serial communication).
6.  **Misc**: Breadboard and Jumper Wires.


## 4. Installation & Setup
1. Hardware Setup
Connect the Push Button to the Arduino:

One leg to GND.

The other leg to Pin D2.

Connect the Arduino to the Raspberry Pi via USB cable.

Connect the Webcam to the Raspberry Pi USB port.

2. Arduino Configuration
Open arduino_node/button_trigger.ino in Arduino IDE.

Select board: Arduino Uno R4 WiFi.

Upload the sketch.

3. Raspberry Pi Environment
Ensure Python 3 is installed.

Install required libraries:

Bash

pip3 install -r requirements.txt
(Note: dlib installation may take time on Raspberry Pi)

4. Facial Database
Create a folder named known_faces inside edge_gateway/.

Add photos of authorized users (e.g., john.jpg, jane.png). The filename will be used as the user's identity.

## 5.How to Run
It is recommended to run the AI Engine and the Dashboard in separate terminal windows.

Step 1: Start the Web Dashboard

Bash

cd edge_gateway
python3 dashboard.py
Access the dashboard at http://<Pi-IP-Address>:8000 on your phone/PC.

Step 2: Start the Edge AI Engine

Bash

# Open a new terminal window
export DISPLAY=:0  # Required if running via SSH to enable GUI
cd edge_gateway
python3 final_main.py
Step 3: Operation

Press the button on the Arduino.

The camera window will pop up on the Pi.

Look at the camera.

Upon successful recognition, check the Web Dashboard for the new log entry.

## 6.License
This project is submitted for the IoT Module COM6017M assessment.
