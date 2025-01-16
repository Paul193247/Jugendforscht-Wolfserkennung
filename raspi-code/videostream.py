from datetime import datetime
import threading
import gi
from time import sleep
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import os
import numpy as np
from PIL import Image
import cv2
import hailo
import signal
import sys
from gpiozero import Button
from hailo_rpi_common import (
    get_caps_from_pad,
    get_numpy_from_buffer,
    app_callback_class,
)
from detection_pipeline import GStreamerDetectionApp

# -----------------------------------------------------------------------------------------------
# User-defined class to be used in the callback function
# -----------------------------------------------------------------------------------------------
# Inheritance from the app_callback_class
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
Gst.init(None)

# Global flag for stopping the pipeline
running = True

# Liste zum Speichern der Frames
frames = []

# Video-Writer-Setup
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # oder 'XVID' für AVI
video_writer = None

# Um ein Signal zu fangen, wenn ^C gedrückt wird
def signal_handler(sig, frame):
    global running
    running = False
    print("Signal empfangen, erstelle Video...")

signal.signal(signal.SIGINT, signal_handler)
def app_callback(pad, info, user_data):
    global frames, video_writer

    # Hole GstBuffer aus info
    buffer = info.get_buffer()
    if buffer is None:
        return Gst.PadProbeReturn.OK

    # Hole Bild-Metadaten und überprüfe nur einmal
    caps = pad.get_current_caps()
    structure = caps.get_structure(0)
    width = structure.get_int('width')[1]
    height = structure.get_int('height')[1]
    format_ = structure.get_string('format')

    if format_ not in {'RGB', 'GRAY8'}:
        print(f"Unsupported format: {format_}")
        return Gst.PadProbeReturn.OK

    # Mappe den Buffer, um Zugriff auf die Daten zu erhalten
    success, map_info = buffer.map(Gst.MapFlags.READ)
    if not success:
        return Gst.PadProbeReturn.OK

    try:
        # Erstelle ein Numpy-Array aus den Rohdaten
        raw_data = np.frombuffer(map_info.data, dtype=np.uint8)

        # Passe die Array-Form nur an, wenn nötig
        if format_ == 'RGB':
            image = raw_data.reshape((height, width, 3))
        elif format_ == 'GRAY8':
            image = raw_data.reshape((height, width))
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)  # In RGB umwandeln, wenn VideoWriter RGB erwartet

        # Extrahiere die Erkennungen
        roi = hailo.get_roi_from_buffer(buffer)
        detections = roi.get_objects_typed(hailo.HAILO_DETECTION)

        # Zeichne Bounding-Boxes und Labels nur, wenn Detections vorhanden sind
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
                # Zeichne die Bounding-Box
                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

                # Zeichne das Label und die Confidence
                cv2.putText(
                    image, f"{label}: {confidence:.2f}",
                    (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1
                )

        # Schreibe das Bild in den Video-Writer
        if video_writer is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_writer = cv2.VideoWriter(f'{timestamp}.mp4', fourcc, 30, (width, height))

        video_writer.write(image)

    finally:
        buffer.unmap(map_info)

    return Gst.PadProbeReturn.OK

def stop_and_save_video():
    global video_writer
    # Wenn die Pipeline gestoppt wird, speichern wir das Video
    print(video_writer)
    if video_writer is not None:
        video_writer.release()
        print("Video wurde gespeichert")

user_data = user_app_callback_class()
try: 
    app = GStreamerDetectionApp(app_callback, user_data, True)
    app.run()
finally:
    stop_and_save_video()