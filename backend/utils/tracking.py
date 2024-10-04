from .config import vehicle_count, vehicle_track
from datetime import datetime
import cv2
import numpy as np

def save_track(cross_in_out, detect, speed_record, dir, in_out, frame):
    for index, data in enumerate(cross_in_out):
        if data == True:
            vehicle = detect.data["class_name"][index] 
            vehicle_count[dir][in_out][vehicle] += 1
            tracker_id = detect.tracker_id[index]
            x1, y1, x2, y2 = detect.xyxy[index]
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            speed = speed_record.get(tracker_id, 0)
            new_data = [tracker_id,detect.data["class_name"][index],x1,y1,x2,y2,f"{dir}_{in_out}",speed,timestamp]
            vehicle_image = frame[int(y1):int(y2), int(x1):int(x2)]
            cv2.imwrite(f"data/images/{dir}/{vehicle}_{tracker_id}_{timestamp}.jpg", vehicle_image)
            vehicle_track.append(new_data)

def calculate_speed(detections, coordinates, fps):
    speed_record = {}
    speed_labels = []
    for tracker_id in detections.tracker_id:
        if len(coordinates[tracker_id]) < fps / 2:
            speed_labels.append(f"#{tracker_id}")
        else:
            coordinate_start_x, coordinate_start_y = coordinates[tracker_id][-1]  # Titik akhir
            coordinate_end_x, coordinate_end_y = coordinates[tracker_id][0]       # Titik awal

            delta_x = abs(coordinate_start_x - coordinate_end_x)
            delta_y = abs(coordinate_start_y - coordinate_end_y)

            # Menghitung jarak Euclidean
            distance = np.sqrt(delta_x**2 + delta_y**2)  # Jarak total dari perubahan x dan y

            time = len(coordinates[tracker_id]) / fps
            speed = distance / time * 3.6
            speed_record[tracker_id] = speed
            speed_labels.append(f"#{tracker_id} {int(speed)} km/h")

    return speed_record, speed_labels
