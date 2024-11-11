import numpy as np
import supervision as sv

simpang_amongrogo_view_timur = {
    "loc" : "simpang_amongrogo_view_timur",
    "video_url" : "https://cctvjss.jogjakota.go.id/atcs/ATCS_Simpang_Amongrogo_View_Timur.stream/chunklist_w14842540.m3u8",
    "LINES_COUNT" : {
        "Nord": (sv.Point(744, 593), sv.Point(1342, 564)),
        "East": (sv.Point(1420, 562), sv.Point(1726, 670)),
        "South": (sv.Point(1716, 859), sv.Point(89, 1031)),
        "West": (sv.Point(89, 1031), sv.Point(345, 682))
    },
    "LINES_RECTANGLE" : [
        sv.Point(335, 567), 
        sv.Point(1383, 520), 
        sv.Point(2450,820), 
        sv.Point(-350, 1250)
    ],
    "SOURCE": np.array([[335, 567], [1383, 520], [2450, 820], [-350, 1250]]),
    "TARGET_WIDTH" : 30,
    "TARGET_HEIGHT" :  27,
    "directories" : ['data/images/simpang_amongrogo_view_timur/Nord', 'data/images/simpang_amongrogo_view_timur/East', 'data/images/simpang_amongrogo_view_timur/West', 'data/images/simpang_amongrogo_view_timur/South', 'video/simpang_amongrogo_view_timur']
}

simpang_demangan_view_utara = {
    "loc" : "simpang_demangan_view_utara",
    "video_url" : "https://cctvjss.jogjakota.go.id/atcs/ATCS_Simpang_Demangan_View_Utara.stream/chunklist_w171558739.m3u8",
    "LINES_COUNT" : {
        "Nord": (sv.Point(410, 320), sv.Point(1360, 311))
    },
    "LINES_RECTANGLE" : [
        sv.Point(802, 82), 
        sv.Point(958, 92), 
        sv.Point(1531,461), 
        sv.Point(235, 521)
    ],
    "SOURCE": np.array([[802, 82], [958, 92], [1531, 461], [235, 521]]),
    "TARGET_WIDTH" : 10,
    "TARGET_HEIGHT" :  150,
    "directories" : ['data/images/simpang_demangan_view_utara/Nord', 'video/simpang_demangan_view_utara']
}


VEHICLE_CLASSES = ["bus", "car", "motorcycle", "truck"]

last_saved_minute = -1
