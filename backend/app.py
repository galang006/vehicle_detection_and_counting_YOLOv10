from flask import Flask, jsonify, request, send_from_directory,  send_file, make_response
import pandas as pd
from flask_cors import CORS
import os

from utils import *

app = Flask(__name__)
CORS(app)

@app.route('/playlist/<path:playlist_name>/<path:filename>.m3u8')
def serve_playlist(playlist_name, filename):
    response = make_response(send_file(f'video/{playlist_name}/{filename}.m3u8'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    return response

@app.route('/playlist/<playlist_name>/segment_<int:segment_number>.ts')
def serve_segment(playlist_name, segment_number):
    try:
        segment_filename = f'video/{playlist_name}/segment_{segment_number:03d}.ts'
        return send_file(segment_filename)
    except Exception as e:
        return {"error": str(e)}, 404

@app.route('/images/<path:loc_name>/<path:direction>/<path:filename>')
def serve_image(loc_name, direction, filename):
    return send_from_directory(f'data/images/{loc_name}/{direction}', filename)

@app.route('/vehicle_track', methods=['GET'])
def filter_vehicle_data():
    loc_name = request.args.get('loc')
    track_id = request.args.get('track_id', type=int) 
    class_name = request.args.get('class_name', type=str) 

    data_file = f'data/vehicle_track_{loc_name}.csv' 
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
        image_path = f"http://127.0.0.1:5000/images/{loc_name}/{direction_folder}/{image_name}"  
    
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
        loc_name = request.args.get('loc')
        csv_file = f'data/vehicle_counts_{loc_name}.csv'

        if not os.path.exists(csv_file):
            return jsonify({"error": "CSV file not found."}), 404

        df_vehicle_count = pd.read_csv(csv_file)
        data_vehicle_count = df_vehicle_count.to_dict(orient='records')
        return jsonify(data_vehicle_count)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/vehicle_track', methods=['GET'])
def get_vehicle_track():
    try:
        loc_name = request.args.get('loc')
        csv_file = f'data/vehicle_track_{loc_name}.csv'

        if not os.path.exists(csv_file):
            return jsonify({"error": "CSV file not found."}), 404

        df_vehicle_track = pd.read_csv(csv_file)
        data_vehicle_track = df_vehicle_track.to_dict(orient='records')
        return jsonify(data_vehicle_track)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)  
