from flask import Flask, jsonify, request, send_from_directory,  send_file, make_response
import pandas as pd
from flask_cors import CORS

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

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('data/images', filename)

@app.route('/vehicle_track', methods=['GET'])
def filter_vehicle_data():
    track_id = request.args.get('track_id', type=int) 
    class_name = request.args.get('class_name', type=str) 

    data_file = 'data/vehicle_track.csv' 
    vehicle_data = pd.read_csv(data_file)

    filtered_data = vehicle_data

    if track_id is not None:
        filtered_data = filtered_data[filtered_data['Track ID'] == track_id]

    if class_name:
        filtered_data = filtered_data[filtered_data['Class Name'] == class_name]

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
