import cv2

def draw_line(frame, start, end, r = 0, g = 0, b=0, thick = 2):
    cv2.line(
        frame,
        (start.x, start.y),
        (end.x, end.y),
        color=(b, g, r),
        thickness=thick
    )

def draw_text_with_background(image, text, position, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.7, font_thickness=2, text_color=(0, 0, 0), bg_color=(0, 255, 255)):
    '''
        Draw a background on the text
    '''
    # Calculate text size
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)
    
    # Draw background
    x, y = position
    rectangle_bgr = bg_color
    cv2.rectangle(image, (x, y - text_height - baseline), (x + text_width, y + baseline), rectangle_bgr, thickness=cv2.FILLED)
    
    # Write Text
    cv2.putText(image, text, (x, y), font, font_scale, text_color, font_thickness)

def generate_vehicle_count_text(vehicle_count_dict):
    return "\n".join([f"{vehicle.capitalize()} In: {vehicle_count_dict['In'][vehicle]}, Out: {vehicle_count_dict['Out'][vehicle]}"
                      for vehicle in vehicle_count_dict['In'].keys()])

def display_vehicle_count(annotated_frame, vehicle_count,title,position, text_color=(0, 0, 0), bg_color=(0, 255, 255)):
    vehicle_count_text = generate_vehicle_count_text(vehicle_count)
    y0, dy = position[1], 30  # Dy for spacing between lines

    # Draw the title for the direction
    cv2.putText(annotated_frame, title, (position[0], y0), cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)

    # Draw the vehicle count below the title
    for i, line in enumerate(vehicle_count_text.split('\n')):
        y = y0 + (i + 1) * dy  # Increment y position for each line
        draw_text_with_background(annotated_frame, line, (position[0], y), text_color=text_color, bg_color=bg_color)
