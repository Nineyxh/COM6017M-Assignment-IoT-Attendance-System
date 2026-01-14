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
