import RPi.GPIO as GPIO
import threading
import gi
import os
import numpy as np
import cv2
import time
import hailo
import signal
import sys
from gpiozero import Button, LED
from time import sleep
from datetime import datetime
from hailo_rpi_common import (
    get_caps_from_pad,
    get_numpy_from_buffer,
    app_callback_class,
)
from detection_pipeline import GStreamerDetectionApp
from SMS import send_message_thread

# -----------------------------------------------------------------------------------------------
# User-defined class to be used in the callback function
# -----------------------------------------------------------------------------------------------
class user_app_callback_class(app_callback_class):
    def __init__(self):
        super().__init__()
        self.new_variable = 42  # New variable example

    def new_function(self):  # New function example
        return "The meaning of life is: "

# -----------------------------------------------------------------------------------------------
# User-defined callback function
# -----------------------------------------------------------------------------------------------

# Initialize GStreamer
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

Gst.init(None)

running = True

frames = []

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = None

def signal_handler(sig, frame):
    global running
    running = False
    print("Signal empfangen, erstelle Video...")

signal.signal(signal.SIGINT, signal_handler)

def draw_boxes(frame, detections):
    """
    Funktion zum Zeichnen von Bounding Boxes auf den erkannten Objekten.
    """
    for detection in detections:
        label = detection.get_label()
        bbox = detection.get_bbox()
        confidence = detection.get_confidence()

        x1, y1, x2, y2 = bbox
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"{label}: {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    return frame

last_wolf = 0
last_dog = 0

last_detections = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

def send_message(animal):
    threading.Thread(target=send_message_thread, args=(animal,)).start()
    print(f"Ein {animal} wurde gesehen!")

def app_callback(pad, info, user_data):
    global frames, video_writer, last_dog, last_wolf, last_detections

    buffer = info.get_buffer()
    if buffer is None:
        return Gst.PadProbeReturn.OK

    format, width, height = get_caps_from_pad(pad)

    frame = None
    if user_data.use_frame and format is not None and width is not None and height is not None:
        frame = get_numpy_from_buffer(buffer, format, width, height)

    roi = hailo.get_roi_from_buffer(buffer)
    detections = roi.get_objects_typed(hailo.HAILO_DETECTION)
    last_detections.append(detections)
    del last_detections[0]
    for detection in detections:
        label = detection.get_label()
        if label == "Wolf" and time.time() - last_wolf >= 600:
            together = 0
            for l in last_detections:
                for d in l:
                    if d.get_label() == "Wolf" and d.get_confidence() > 0.5:
                        together += 1
            avg = together / len(last_detetions)
            if avg > 0.5:
                last_wolf = time.time()
                send_message(label)
        if label == "Hund" and time.time() - last_dog >= 600:
            together = 0
            for l in last_detections:
                for d in l:
                    if d.get_label() == "Hund" and d.get_confidence() > 0.5:
                        together += 1
            avg = together / len(last_detections)
            if avg > 0.5:
                last_dog = time.time()
                send_message(label)

    caps = pad.get_current_caps()
    structure = caps.get_structure(0)
    width = structure.get_int('width')[1]
    height = structure.get_int('height')[1]
    format_ = structure.get_string('format')

    if format_ not in {'RGB', 'GRAY8'}:
        print(f"Unsupported format: {format_}")
        return Gst.PadProbeReturn.OK

    success, map_info = buffer.map(Gst.MapFlags.READ)
    if not success:
        return Gst.PadProbeReturn.OK

    try:
        raw_data = np.frombuffer(map_info.data, dtype=np.uint8)

        if format_ == 'RGB':
            image = raw_data.reshape((height, width, 3))
        elif format_ == 'GRAY8':
            image = raw_data.reshape((height, width))
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

        roi = hailo.get_roi_from_buffer(buffer)
        detections = roi.get_objects_typed(hailo.HAILO_DETECTION)

        if detections:
            for detection in detections:
                label = detection.get_label()
                print(label)
                bbox = detection.get_bbox()
                confidence = detection.get_confidence()

                xmin = int(bbox.xmin() * width)
                xmax = int(bbox.xmax() * width)
                ymin = int(bbox.ymin() * height)
                ymax = int(bbox.ymax() * height)
                image = image.copy()
                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

                cv2.putText(
                    image, f"{label}: {confidence:.2f}",
                    (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1
                )

        if video_writer is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_writer = cv2.VideoWriter(f'{timestamp}.mp4', fourcc, 30, (width, height))

        video_writer.write(image)

    finally:
        buffer.unmap(map_info)

    return Gst.PadProbeReturn.OK

zustand = 0

button = Button(23)


thread = None
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN)
user_data = None
app = None

def start():
    print("Pipeline started")
    GPIO.setup(24, GPIO.OUT)
    app.run()

def stop_and_save_video():
    global video_writer
    if video_writer is not None:
        video_writer.release()
        print("Video wurde gespeichert")
    video_writer = None

motion = False

i = 0
try:
    while True:
        if i > 2000000:
            motion = False
        else:
            motion = True
        if button.is_pressed:
            i += 1
        else:
            i = 0
        if zustand == 0 and motion:
            zustand = 1
            user_data = user_app_callback_class()
            app = GStreamerDetectionApp(app_callback, user_data, False)
            thread = threading.Thread(target=start)
            thread.start()
        if zustand == 1 and not motion:
            zustand = 0
            app.shutdown()
            thread.join()
            stop_and_save_video()
            GPIO.setup(24, GPIO.IN)
            print("Pipeline gestoppt")
finally:
    GPIO.setup(24, GPIO.IN)
