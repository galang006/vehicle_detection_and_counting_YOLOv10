from collections import defaultdict, deque

import cv2
from ultralytics import YOLO
import supervision as sv
from datetime import datetime
import os
from .config import *
from utils import save_data_to_csv, ViewTransformer, save_track, draw_line, display_vehicle_count, calculate_speed, signal_handler, check_last_id
import subprocess
import signal
from copy import deepcopy 


def vehicle_detection(location):
    video_url = location["video_url"]
    LINES_COUNT = location["LINES_COUNT"]
    LINES_RECTANGLE = location["LINES_RECTANGLE"]
    SOURCE = location["SOURCE"]
    directories = location["directories"]
    TARGET_WIDTH = location["TARGET_WIDTH"]
    TARGET_HEIGHT = location["TARGET_HEIGHT"]
    loc_name = location["loc"]
    output_dir = f'video/{loc_name}'

    last_id = check_last_id(loc_name)
    global last_saved_minute

    TARGET = np.array(
        [
            [0, 0],
            [TARGET_WIDTH - 1, 0],
            [TARGET_WIDTH - 1, TARGET_HEIGHT - 1],
            [0, TARGET_HEIGHT - 1],
        ]
    )
    vehicle_count = {
        zone: {
            "In": {cls: 0 for cls in VEHICLE_CLASSES}, 
            "Out": {cls: 0 for cls in VEHICLE_CLASSES}
        } 
        for zone in LINES_COUNT.keys()
    }
    vehicle_track = []

    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, vehicle_count, vehicle_track))

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

    cap = cv2.VideoCapture(video_url)
    
    if not cap.isOpened():
        print("Error: Tidak bisa membuka streaming video.")
        exit()

    video_info = sv.VideoInfo(
        fps=int(cap.get(cv2.CAP_PROP_FPS)),
        width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )

    ffmpeg_process = subprocess.Popen([
        'ffmpeg',
        '-y',  # overwrite existing files
        '-f', 'rawvideo',  # input format
        '-vcodec', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', f'{video_info.width}x{video_info.height}',  # input size
        '-r', str(video_info.fps),  # frame rate
        '-i', '-',  # input comes from stdin
        '-c:v', 'libx264',  # codec
        '-f', 'hls',  # format HLS
        '-hls_time', '10',  # duration of each segment
        '-hls_list_size', '6',  # ensure all segments are listed
        '-hls_flags', 'delete_segments+append_list',  # dynamically update playlist and remove old segments
        '-hls_segment_filename', os.path.join(output_dir, 'segment_%03d.ts'),  # segment file pattern
        os.path.join(output_dir, f'{loc_name}.m3u8')  # m3u8 playlist
    ], stdin=subprocess.PIPE)

    model = YOLO('models/best.pt')

    byte_track = sv.ByteTrack(
        frame_rate=video_info.fps
    )

    thickness = sv.calculate_optimal_line_thickness(resolution_wh=video_info.resolution_wh)
    text_scale = sv.calculate_optimal_text_scale(resolution_wh=video_info.resolution_wh)
    box_annotator = sv.BoxAnnotator(thickness=thickness)
    label_annotator = sv.LabelAnnotator(
        text_scale=text_scale,
        text_thickness=thickness,
        text_position=sv.Position.BOTTOM_CENTER,
    )

    trace_annotator = sv.TraceAnnotator(
        thickness=thickness,
        trace_length=video_info.fps * 2,
        position=sv.Position.BOTTOM_CENTER,
    )

    line_zones = {
        zone_name: [
            sv.LineZone(start=line_coordinates[0], end=line_coordinates[1],
                        triggering_anchors=[sv.Position.BOTTOM_CENTER]),
            zone_name
        ]
        for zone_name, line_coordinates in LINES_COUNT.items()
    }

    polygon_zone = sv.PolygonZone(polygon=SOURCE)
    view_transformer = ViewTransformer(source=SOURCE, target=TARGET)

    coordinates = defaultdict(lambda: deque(maxlen=video_info.fps))
    
    while True:
        try:
            ret, frame = cap.read()
            if not ret:
                print("Error: Tidak dapat membaca frame dari streaming.")
                break

            result = model(frame)[0]
            detections = sv.Detections.from_ultralytics(result)
            detections = detections[detections.confidence > 0.5]
            detections = detections[polygon_zone.trigger(detections)]
            detections = detections.with_nms(threshold=0.7)
            detections = byte_track.update_with_detections(detections=detections)

            points = detections.get_anchors_coordinates(anchor=sv.Position.BOTTOM_CENTER)
            points = view_transformer.transform_points(points=points).astype(int)

            for tracker_id, (x, y) in zip(detections.tracker_id, points):
                coordinates[tracker_id].append((x, y))
    
            speed_record, labels = calculate_speed(detections, coordinates, video_info.fps)

            for zone_name, line_zone in line_zones.items():
                crossed_in, crossed_out = line_zone[0].trigger(detections)
                save_track(crossed_in, detections, last_id ,speed_record, dir=line_zone[1], in_out="In", frame=frame, loc_name=loc_name,vehicle_count=vehicle_count, vehicle_track=vehicle_track)
                save_track(crossed_out, detections, last_id ,speed_record, dir=line_zone[1], in_out="Out", frame=frame,loc_name=loc_name ,vehicle_count=vehicle_count, vehicle_track=vehicle_track)

            annotated_frame = frame.copy()
            annotated_frame = trace_annotator.annotate(scene=annotated_frame, detections=detections)
            annotated_frame = box_annotator.annotate(scene=annotated_frame, detections=detections)
            annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)

            for i in range(len(LINES_RECTANGLE)):
                draw_line(annotated_frame, LINES_RECTANGLE[i], LINES_RECTANGLE[(i+1)% len(LINES_RECTANGLE)])

            for zone_name, line_coor in LINES_COUNT.items():
                draw_line(annotated_frame, line_coor[0], line_coor[1])
            
            x = 10
            for zone_name, value in vehicle_count.items():
                display_vehicle_count(annotated_frame, vehicle_count[zone_name], zone_name, position=(x, 80), bg_color=(0, 255, 0))
                x += 300

            current_time = datetime.now()
            if current_time.minute % 5 == 0 and current_time.second == 0 and current_time.minute != last_saved_minute:
                vehicle_track = save_data_to_csv(vehicle_count, vehicle_track, loc_name)
                last_saved_minute = current_time.minute  

            ffmpeg_process.stdin.write(annotated_frame.tobytes())

        except Exception as e:
            print(f"An error occurred: {e}")
            save_data_to_csv(vehicle_count, vehicle_track, loc_name)
            break    

    cap.release()
    ffmpeg_process.stdin.close()
    ffmpeg_process.wait()


def display_detection(location):
    video_url = location["video_url"]
    LINES_COUNT = location["LINES_COUNT"]
    LINES_RECTANGLE = location["LINES_RECTANGLE"]
    SOURCE = location["SOURCE"]
    directories = location["directories"]
    TARGET_WIDTH = location["TARGET_WIDTH"]
    TARGET_HEIGHT = location["TARGET_HEIGHT"]
    loc_name = location["loc"]
    last_id = check_last_id(loc_name)

    global last_saved_minute

    TARGET = np.array(
        [
            [0, 0],
            [TARGET_WIDTH - 1, 0],
            [TARGET_WIDTH - 1, TARGET_HEIGHT - 1],
            [0, TARGET_HEIGHT - 1],
        ]
    )
 
    vehicle_count = {
        zone: {
            "In": {cls: 0 for cls in VEHICLE_CLASSES}, 
            "Out": {cls: 0 for cls in VEHICLE_CLASSES}
        } 
        for zone in LINES_COUNT.keys()
    }
    vehicle_track = []

    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, vehicle_count, vehicle_track))
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

    cap = cv2.VideoCapture(video_url)
    fps = cap.get(cv2.CAP_PROP_FPS)

    delay = int(1000 / fps)

    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    if not cap.isOpened():
        print("Error: Tidak bisa membuka streaming video.")
        exit()

    video_info = sv.VideoInfo(
        fps=int(cap.get(cv2.CAP_PROP_FPS)),
        width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )

    model = YOLO('models/best.pt')

    byte_track = sv.ByteTrack(
        frame_rate=video_info.fps
    )

    thickness = sv.calculate_optimal_line_thickness(resolution_wh=video_info.resolution_wh)
    text_scale = sv.calculate_optimal_text_scale(resolution_wh=video_info.resolution_wh)
    box_annotator = sv.BoxAnnotator(thickness=thickness)
    label_annotator = sv.LabelAnnotator(
        text_scale=text_scale,
        text_thickness=thickness,
        text_position=sv.Position.BOTTOM_CENTER,
    )

    trace_annotator = sv.TraceAnnotator(
        thickness=thickness,
        trace_length=video_info.fps * 2,
        position=sv.Position.BOTTOM_CENTER,
    )

    line_zones = {
        zone_name: [
            sv.LineZone(start=line_coordinates[0], end=line_coordinates[1],
                        triggering_anchors=[sv.Position.BOTTOM_CENTER]),
            zone_name
        ]
        for zone_name, line_coordinates in LINES_COUNT.items()
    }

    polygon_zone = sv.PolygonZone(polygon=SOURCE)
    view_transformer = ViewTransformer(source=SOURCE, target=TARGET)

    coordinates = defaultdict(lambda: deque(maxlen=video_info.fps))
    
    while True:
        try:
            ret, frame = cap.read()
            if not ret:
                print("Error: Tidak dapat membaca frame dari streaming.")
                break

            result = model(frame)[0]
            detections = sv.Detections.from_ultralytics(result)
            detections = detections[detections.confidence > 0.5]
            detections = detections[polygon_zone.trigger(detections)]
            detections = detections.with_nms(threshold=0.7)
            detections = byte_track.update_with_detections(detections=detections)

            points = detections.get_anchors_coordinates(anchor=sv.Position.BOTTOM_CENTER)
            points = view_transformer.transform_points(points=points).astype(int)

            for tracker_id, (x, y) in zip(detections.tracker_id, points):
                coordinates[tracker_id].append((x, y))
    
            speed_record, labels = calculate_speed(detections, coordinates, video_info.fps)

            for zone_name, line_zone in line_zones.items():
                crossed_in, crossed_out = line_zone[0].trigger(detections)
                save_track(crossed_in, detections, last_id ,speed_record, dir=line_zone[1], in_out="In", frame=frame, loc_name=loc_name,vehicle_count=vehicle_count, vehicle_track=vehicle_track)
                save_track(crossed_out, detections, last_id ,speed_record, dir=line_zone[1], in_out="Out", frame=frame,loc_name=loc_name ,vehicle_count=vehicle_count, vehicle_track=vehicle_track)

            annotated_frame = frame.copy()
            annotated_frame = trace_annotator.annotate(scene=annotated_frame, detections=detections)
            annotated_frame = box_annotator.annotate(scene=annotated_frame, detections=detections)
            annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)

            for i in range(len(LINES_RECTANGLE)):
                draw_line(annotated_frame, LINES_RECTANGLE[i], LINES_RECTANGLE[(i+1)% len(LINES_RECTANGLE)])

            for zone_name, line_coor in LINES_COUNT.items():
                draw_line(annotated_frame, line_coor[0], line_coor[1])
            
            x = 10
            for zone_name, value in vehicle_count.items():
                display_vehicle_count(annotated_frame, vehicle_count[zone_name], zone_name, position=(x, 80), bg_color=(0, 255, 0))
                x += 300

            cv2.imshow("frame", annotated_frame)

            current_time = datetime.now()
            if current_time.minute % 5 == 0 and current_time.second == 0 and current_time.minute != last_saved_minute:
                vehicle_track = save_data_to_csv(vehicle_count, vehicle_track, loc_name)
                last_saved_minute = current_time.minute  
        
            if cv2.waitKey(delay) & 0xFF == 27:  
                save_data_to_csv(vehicle_count, vehicle_track, loc_name)
                break

        except Exception as e:
            print(f"An error occurred: {e}")
            save_data_to_csv(vehicle_count, vehicle_track, loc_name)
            break    

    cap.release()
    cv2.destroyAllWindows()
