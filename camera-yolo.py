import cv2
import time
import threading
from picamera2 import Picamera2
from ultralytics import YOLO
from sense_hat import SenseHat

# 1. Initialize Hardware & Model
sense = SenseHat()
sense.clear()
model = YOLO('yolov8n-head.pt')

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (1280, 720)})
picam2.configure(config)
picam2.start()

# Thresholds
MAX_OCCUPANCY = 4
alert_active = False

def yellow_alert():
    """Background thread to flash yellow without lagging the camera."""
    global alert_active
    alert_active = True
    yellow = [255, 255, 0]
    off = [0, 0, 0]
    
    # Simple flash pattern
    for _ in range(3):
        sense.clear(yellow)
        time.sleep(0.3)
        sense.clear(off)
        time.sleep(0.3)
        
    alert_active = False

print("System Active... Press 'q' to quit")

try:
    while True:
        # Capture frame
        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Ensure 3 channels
        if frame.shape[2] == 4:
            frame = frame[:, :, :3]
        
        # Get Environment Data
        temp = sense.get_temperature()
        humidity = sense.get_humidity()
        
        # 2. Detection (class 0 is person)
        results = model.predict(frame, classes=[0], conf=0.6, imgsz=320, verbose=False)
        count = len(results[0].boxes)
        
        # 3. Trigger "Gentle" Alert if crowded
        if count > MAX_OCCUPANCY and not alert_active:
            threading.Thread(target=yellow_alert, daemon=True).start()

        # 4. Visuals for Preview
        annotated_frame = results[0].plot()
        
        # Overlay Text
        y_offset = 30
        info_text = [
            f"Count: {count}",
            f"Temp: {temp:.1f}C",
            f"Humid: {humidity:.1f}%"
        ]
        
        for i, text in enumerate(info_text):
            cv2.putText(annotated_frame, text, (15, y_offset + (i * 30)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        cv2.imshow('Smart Ward Monitor', annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    picam2.stop()
    cv2.destroyAllWindows()
    sense.clear()
