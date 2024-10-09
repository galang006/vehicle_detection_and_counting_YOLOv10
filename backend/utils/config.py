import numpy as np
import supervision as sv

video_url = "https://cctvjss.jogjakota.go.id/atcs/ATCS_Simpang_Amongrogo_View_Timur.stream/chunklist_w14842540.m3u8"

LINES_COUNT = {
    "Nord": (sv.Point(744, 593), sv.Point(1342, 564)),
    "West": (sv.Point(89, 1031), sv.Point(345, 682)),
    "East": (sv.Point(1420, 562), sv.Point(1726, 670)),
    "South": (sv.Point(1716, 859), sv.Point(89, 1031))
}

LINES_RECTANGLE = [
    sv.Point(335, 567), 
    sv.Point(1383, 520), 
    sv.Point(2450,820), 
    sv.Point(-350, 1250)
]
  
SOURCE = np.array([[335, 567], [1383, 520], [2450, 820], [-350, 1250]])
TARGET_WIDTH, TARGET_HEIGHT= 30, 21.5

VEHICLE_CLASSES = ["bus", "car", "motorcycle", "truck"]

directories = ['data/images', 'data/images/Nord', 'data/images/East', 'data/images/West', 'data/images/South']

vehicle_count = {
    "Nord": {"In": {cls: 0 for cls in VEHICLE_CLASSES}, "Out": {cls: 0 for cls in VEHICLE_CLASSES}},
    "East": {"In": {cls: 0 for cls in VEHICLE_CLASSES}, "Out": {cls: 0 for cls in VEHICLE_CLASSES}},
    "South": {"In": {cls: 0 for cls in VEHICLE_CLASSES}, "Out": {cls: 0 for cls in VEHICLE_CLASSES}},
    "West": {"In": {cls: 0 for cls in VEHICLE_CLASSES}, "Out": {cls: 0 for cls in VEHICLE_CLASSES}},
}

last_saved_minute = -1

vehicle_track = []

TARGET = np.array(
    [
        [0, 0],
        [TARGET_WIDTH - 1, 0],
        [TARGET_WIDTH - 1, TARGET_HEIGHT - 1],
        [0, TARGET_HEIGHT - 1],
    ]
)
