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
    directions = vehicle_count.keys()
    data = {'Class': VEHICLE_CLASSES}

    for direction in directions:
        data[f'{direction} In'] = [vehicle_count[direction]['In'].get(vehicle, 0) for vehicle in VEHICLE_CLASSES]
        data[f'{direction} Out'] = [vehicle_count[direction]['Out'].get(vehicle, 0) for vehicle in VEHICLE_CLASSES]

    data['timestamp'] = [current_time] * len(VEHICLE_CLASSES)
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

def check_last_id(loc_name):
    csv_file = f'data/vehicle_track_{loc_name}.csv'

    try:
        df = pd.read_csv(csv_file)
        largest_track_id = df['Track ID'].max()  
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
        largest_track_id = 0
    except Exception as e:
        print(f"An error occurred: {e}")
        largest_track_id = 0
    
    return largest_track_id