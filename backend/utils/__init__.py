from .tracking import save_track, calculate_speed, check_track_exists
from .view_transformer import ViewTransformer
from .display import draw_line, draw_text_with_background, display_vehicle_count, generate_vehicle_count_text
from .save_to_csv import save_data_to_csv, signal_handler, check_last_id
#from .config import video_url, LINES_COUNT, LINES_RECTANGLE, SOURCE, TARGET, directories, VEHICLE_CLASSES, count, TARGET_WIDTH, TARGET_HEIGHT, last_saved_minute
from .config import simpang_amongrogo_view_timur, VEHICLE_CLASSES, last_saved_minute, simpang_demangan_view_utara
from .detection import vehicle_detection, display_detection