from flask import Flask, jsonify, request, Response, send_from_directory,  send_file, make_response
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

@app.route('/playlist.m3u8')
def serve_playlist():
    response = make_response(send_file('video/playlist.m3u8'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    return response

@app.route('/segment_<int:segment_number>.ts')
def serve_segment(segment_number):
    segment_filename = f'video/segment_{segment_number:03d}.ts'
    return send_file(segment_filename)


# @app.route('/vehicle_track/<track_id>', methods=['GET'])
# def get_vehicle_by_track_id(track_id):
#     data_file = 'data/vehicle_track.csv'  # Update this to your CSV file path
#     vehicle_data = pd.read_csv(data_file)
#     # Filter the vehicle data based on Track ID
#     track_id_int = int(track_id)  # Convert to integer for filtering
    
#     # Filter the vehicle data based on Track ID
#     filtered_data = vehicle_data[vehicle_data['Track ID'] == track_id_int]

#     if not filtered_data.empty:
#         return jsonify(filtered_data.to_dict(orient='records'))
#     else:
#         return jsonify({'message': 'No data found for the given Track ID'}), 404

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('data/images', filename)

@app.route('/vehicle_track', methods=['GET'])
def filter_vehicle_data():
    track_id = request.args.get('track_id', type=int)  # Get Track ID as integer
    class_name = request.args.get('class_name', type=str)  # Get Class Name

    data_file = 'data/vehicle_track.csv'  # Update this to your CSV file path
    vehicle_data = pd.read_csv(data_file)

    # Start filtering based on provided parameters
    filtered_data = vehicle_data

    if track_id is not None:
        filtered_data = filtered_data[filtered_data['Track ID'] == track_id]

    if class_name:
        filtered_data = filtered_data[filtered_data['Class Name'] == class_name]

    # Construct the image URLs 
    image_urls = []
    for _, row in filtered_data.iterrows():
        direction_folder = row['Direction'].split('_')[0]
        image_name = f"{row['Class Name']}_{row['Track ID']}_{row['Timestamp']}.jpg"
        image_path = f"http://127.0.0.1:5000/images/{direction_folder}/{image_name}"
        
        image_urls.append({
            'Track ID': row['Track ID'],
            'Image URL': image_path
        })

    if not filtered_data.empty:
        filtered_data_list = filtered_data.to_dict(orient='records')
        for i, item in enumerate(filtered_data_list):
            item['Image URL'] = image_urls[i]['Image URL'] if i < len(image_urls) else None
        
        return jsonify(filtered_data_list)
    else:
        return jsonify({'message': 'No data found for the given filters'}), 404

# @app.route('/vehicle_track', methods=['GET'])
# def filter_vehicle_data():
#     track_id = request.args.get('track_id', type=int)  # Get Track ID as integer
#     class_name = request.args.get('class_name', type=str)  # Get Class Name
#     timestamp = request.args.get('timestamp', type=str)  # Get Timestamp
#     direction = request.args.get('direction', type=str)  # Get Direction

#     data_file = 'data/vehicle_track.csv'  # Update this to your CSV file path
#     vehicle_data = pd.read_csv(data_file)

#     # Start filtering based on provided parameters
#     filtered_data = vehicle_data

#     if track_id is not None:
#         filtered_data = filtered_data[filtered_data['Track ID'] == track_id]

#     if class_name:
#         filtered_data = filtered_data[filtered_data['Class Name'] == class_name]

#     if timestamp:
#         filtered_data = filtered_data[filtered_data['Timestamp'] == timestamp]

#     if direction:
#         # Extract the word before the underscore for filtering
#         direction_prefix = direction.split('_')[0]
#         filtered_data = filtered_data[filtered_data['Direction'].str.startswith(direction_prefix)]
# # Construct the image URLs for the filtered data
#     base_image_path = 'data/images/'  # Base path for the images
#     image_urls = []

#     for _, row in filtered_data.iterrows():
#         # Construct the directory and image filename
#         direction_folder = row['Direction'].split('_')[0]  # Get the direction prefix
#         image_name = f"{row['Class Name']}_{row['Track ID']}_{row['Timestamp']}.jpg"  # Assuming jpg format
#         image_path = f"{base_image_path}{direction_folder}/{image_name}"  # Complete path
        
#         # Add the image URL to the row data
#         image_urls.append({
#             'Track ID': row['Track ID'],
#             'Image URL': image_path  # Add the image URL
#         })

#     if not filtered_data.empty:
#         # Convert filtered data to a list of dictionaries
#         filtered_data_list = filtered_data.to_dict(orient='records')
        
#         # Add image URLs to the filtered data
#         for i, item in enumerate(filtered_data_list):
#             item['Image URL'] = image_urls[i]['Image URL'] if i < len(image_urls) else None
        
#         return jsonify(filtered_data_list)
#     else:
#         return jsonify({'message': 'No data found for the given filters'}), 404

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
