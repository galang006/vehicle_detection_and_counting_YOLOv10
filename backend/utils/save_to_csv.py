from datetime import datetime
from .config import VEHICLE_CLASSES
import pandas as pd
import os

def signal_handler(sig, frame, vehicle_count, vehicle_track):
    print("Keyboard interrupt detected. Saving data...")
    save_data_to_csv(vehicle_count, vehicle_track)
    print("Data successfully saved.")
    exit(0)

def save_data_to_csv(vehicle_count, vehicle_track, loc_name):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {
        'Class': list(vehicle_count['Nord']['In'].keys()), 
        'Nord In': [vehicle_count['Nord']['In'].get(vehicle, 0) for vehicle in VEHICLE_CLASSES],
        'Nord Out': [vehicle_count['Nord']['Out'].get(vehicle, 0) for vehicle in VEHICLE_CLASSES],
        'East In': [vehicle_count['East']['In'].get(vehicle, 0) for vehicle in VEHICLE_CLASSES],
        'East Out': [vehicle_count['East']['Out'].get(vehicle, 0) for vehicle in VEHICLE_CLASSES],
        'South In': [vehicle_count['South']['In'].get(vehicle, 0) for vehicle in VEHICLE_CLASSES],
        'South Out': [vehicle_count['South']['Out'].get(vehicle, 0) for vehicle in VEHICLE_CLASSES],
        'West In': [vehicle_count['West']['In'].get(vehicle, 0) for vehicle in VEHICLE_CLASSES],
        'West Out': [vehicle_count['West']['Out'].get(vehicle, 0) for vehicle in VEHICLE_CLASSES],
        'timestamp': [current_time] * len(VEHICLE_CLASSES)
    }
    df_counts = pd.DataFrame(data)

    df_track = pd.DataFrame(vehicle_track, columns=['Track ID', 'Class Name', 'x1', 'y1', 'x2', 'y2', 'Direction', 'Speed', 'Timestamp'])

    file_path = f'data/vehicle_counts_{loc_name}.csv'
    track_file_path = f'data/vehicle_track_{loc_name}.csv'

    try:
        if not os.path.exists(file_path):
            df_counts.to_csv(file_path, index=False)
        else:
            df_counts.to_csv(file_path, mode='a', header=False, index=False)

        if not os.path.exists(track_file_path):
            df_track.to_csv(track_file_path, index=False)
        else:
            df_track.to_csv(track_file_path, mode='a', header=False, index=False)

        print(f"Data successfully saved at {current_time}")

    except PermissionError:
        print(f"Permission denied: Unable to write to {file_path} or {track_file_path}. Please close the file if it is open or check file permissions.")
    except Exception as e:
        print(f"An error occurred while saving the data: {e}")

    return []
