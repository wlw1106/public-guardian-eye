# Public Guardian Eye
<img src="img/3442-01.gif" width="300"><img src="img/3442-02.gif" width="300"><br>

## Overview
Public Guardian Eye is an embedded system designed for hospital ward visitor management. By automating visitor count monitoring, it reduces the management burden on medical staff and prevents overcrowding. Additionally, the system integrates temperature and humidity sensors to ensure that wards maintain a comfortable and healthy environment.

## Key Features
* **AI People Counting:** Utilizes a YOLOv8-head model (Nano version, specifically for head counting) for real-time pedestrian detection.
* **Environmental Data Acquisition:** Reads real-time temperature and humidity data via the SenseHat.
* **Non-blocking Alert System:** Automatically triggers an alarm when the number of visitors exceeds the defined threshold (MAX_OCCUPANCY). The alert displays flashing lighting on the 8x8 built-in LED matrix on the SenseHat.
* **Edge-AI Privacy:** All visual data is processed locally on the edge device to ensure that patient and visitor privacy is fully secured.

## Hardware Setup & Installation
* **Camera Positioning:** The system is optimized for a ceiling-mounted or top-corner installation.
* **Optimal Angle:** The camera is set at a 45° tilt angle to provide the optimal field of view for human head detection.
* **Thermal Management:** Running highly demanding AI models like YOLOv8 causes the Raspberry Pi's CPU to generate significant heat. Because the SenseHat is typically close to the main PCB motherboard, its sensor readings can be affected by this self-heating effect. It is strongly suggested to use an external ribbon cable to extend the GPIO of the Pi, separating the SenseHat from the CPU heat source.

## Software Architecture
* **Finite State Machine (FSM):** The core logic transitions between INIT, MONITORING, ALERTING, and EXIT/SHUTDOWN states.
* **Asynchronous Control Logic:** Employs non-blocking threading for the alert system to ensure concurrency and maintain real-time camera framing and inference.
* **Hardware Interfacing:** Utilizes I/O polling for continuous environmental checks.
* **Defensive Design & Resource Deallocation:** Implements a standard `try...finally` approach to prevent partial failures from crashing the entire program. This ensures that crucial deallocation steps (`picam2.stop()`, `cv2.destroyAllWindows()`, `sense.clear()`) are always executed.

## Future Improvements
* **Dynamic Thresholding:** The current iteration uses a hard-coded, non-dynamic threshold to ensure the demonstration runs smoothly without setup delays. Future updates will implement a dynamic approach featuring auto-calibration during non-visiting hours, calculating maximum visitors based on the active patient count.

## Dependencies
* Python 3.x
* `opencv-python` (cv2)
* `picamera2`
* `ultralytics` (YOLOv8)
* `sense_hat`
