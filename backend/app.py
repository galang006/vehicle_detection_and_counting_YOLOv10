from flask import Flask, jsonify, request, Response
import subprocess
import os
import pandas as pd
from flask_cors import CORS
from collections import defaultdict, deque

import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv
from datetime import datetime
from utils import *

app = Flask(__name__)
CORS(app)

@app.route('/start_stream', methods=['GET'])
def start_stream():
    return Response(vehicle_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/start_stream', methods=['GET'])
# def start_stream():
#     def generate_frames():
#         cap = cv2.VideoCapture(video_url)

#         model = YOLO('models/best.pt')  # Load your YOLO model here
#         box_annotator = sv.BoxAnnotator()
#         label_annotator = sv.LabelAnnotator()

#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             result = model(frame)[0]
#             detections = sv.Detections.from_ultralytics(result)
#             detections = detections[detections.confidence > 0.5]
            
#             # Annotate your frame (add detection boxes, labels, etc.)
#             # Use supervision library functions to draw bounding boxes, labels, etc.

#             # Encode frame as JPEG
#             frame = box_annotator.annotate(scene=frame, detections=detections)
#             frame = label_annotator.annotate(scene=frame, detections=detections)
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()

#             # Yield frame for response stream
#             yield (b'--frame\r\n'
#                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/vehicle_count', methods=['GET'])
def get_vehicle_count():
    try:
        df_vehicle_count = pd.read_csv('data/vehicle_counts.csv')
        data_vehicle_count = df_vehicle_count.to_dict(orient='records')
        return jsonify(data_vehicle_count)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/vehicle_track', methods=['GET'])
def get_vehicle_track():
    try:
        df_vehicle_track = pd.read_csv('data/vehicle_track.csv')
        data_vehicle_track = df_vehicle_track.to_dict(orient='records')
        return jsonify(data_vehicle_track)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)  
