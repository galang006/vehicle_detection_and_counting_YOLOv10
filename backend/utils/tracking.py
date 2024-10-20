from datetime import datetime
import cv2
import numpy as np
import pandas as pd

def save_track(cross_in_out, detect, last_id,speed_record, dir, in_out, frame, loc_name, vehicle_count, vehicle_track):
    for index, data in enumerate(cross_in_out):
        if data == True:
            vehicle = detect.data["class_name"][index] 
            vehicle_count[dir][in_out][vehicle] += 1
            tracker_id = detect.tracker_id[index] + last_id
            if(not check_track_exists(loc_name, tracker_id, f"{dir}_{in_out}")):
                x1, y1, x2, y2 = detect.xyxy[index]
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                speed = round(speed_record.get(tracker_id-last_id, 0), 2)
                new_data = [tracker_id,detect.data["class_name"][index],round(x1, 1),round(y1, 1),round(x2, 1),round(y2, 1),f"{dir}_{in_out}",speed,timestamp]
                vehicle_image = frame[int(y1):int(y2), int(x1):int(x2)]
                cv2.imwrite(f"data/images/{loc_name}/{dir}/{vehicle}_{tracker_id}_{timestamp}.jpg", vehicle_image)
                vehicle_track.append(new_data)

def calculate_speed(detections, coordinates, fps):
    speed_record = {}
    speed_labels = []
    for tracker_id in detections.tracker_id:
        if len(coordinates[tracker_id]) < fps / 2:
            speed_labels.append(f"#{tracker_id}")
        else:
            coordinate_start_x, coordinate_start_y = coordinates[tracker_id][-1]  
            coordinate_end_x, coordinate_end_y = coordinates[tracker_id][0]      

            delta_x = abs(coordinate_start_x - coordinate_end_x)
            delta_y = abs(coordinate_start_y - coordinate_end_y)

            distance = np.sqrt(delta_x**2 + delta_y**2)  

            time = len(coordinates[tracker_id]) / fps
            speed = distance / time * 3.6
            speed_record[tracker_id] = speed
            speed_labels.append(f"#{tracker_id} {int(speed)} km/h")

    return speed_record, speed_labels


def check_track_exists(loc_name, track_id, dir_name):
    csv_file = f'data/vehicle_track_{loc_name}.csv'
    
    try:
        df = pd.read_csv(csv_file)

        exists = not df[(df['Track ID'] == track_id) & (df['Direction'] == dir_name)].empty
        
        return exists
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False