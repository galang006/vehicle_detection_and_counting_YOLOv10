# Vehicle Detection and Counting System

This project is a real-time vehicle detection, tracking, and counting system designed for traffic monitoring. The system is implemented using OpenCV for image processing and Flask for API management. It processes video streams, tracks vehicle entries and exits from defined zones, and provides vehicle counts in each direction.

## Features

- **Real-time Vehicle Detection**: Detects vehicles from video feeds using pre-defined zones.
- **Vehicle Tracking and Counting**: Tracks and counts vehicles in each direction, updating dynamically as they enter and exit designated zones.
- **REST API Integration**: API endpoints in Flask allow triggering the vehicle detection process and streaming video content.
- **Data Logging**: Stores vehicle count data and tracking logs in CSV files for later analysis.

## Prerequisites

- Python 3.11+
- OpenCV
- Flask
- Pandas
- Numpy
- Supervision
- Ultralytics

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/galang006/vehicle_project.git
    cd vehicle_project
    ```

## Usage

1. Run the Flask API Server:
    - First, navigate to the backend directory:
    ```sh
    cd backend
    ```
    - Run the Flask API server with:
    ```sh
    python app.py
    ```
    The Flask app will start on http://127.0.0.1:5000
   
2. Generate Detection Playlists:
    - While still in the backend directory, generate the detection playlist by running:
    ```sh
    python main.py
    ```
    - This command processes the video feed to detect vehicles, create playlists, and save results in the video/ folder. Ensure the configuration in main.py aligns with the desired detection settings and input videos.
  
3. Start the Frontend:
    - Open a new terminal window or navigate back to the project root, then enter the frontend directory:
    ```sh
    cd frontend
    ```
    - Run the frontend application with:
    ```sh
    npm start
    ```
    - The frontend will launch, displaying the web interface for the vehicle detection system. Follow on-screen instructions to view the video streams and vehicle detection results.

## Code Structure

1. Backend (backend/):
    - `app.py`: The main Flask API application file, handling API routes. This includes the /playlist route to serve m3u8 files and trigger vehicle detection.
    - `main.py`: The script for generating vehicle detection playlists.
    - `utils/`: A folder containing utility modules. For instance:
        - `config.py`: Contains configurations for different video sources, lines for counting vehicles, and directory paths for storing images and data.
        - `detection.py`: Implements vehicle_detection function and other detection logic.
        - `tracking.py`: Provides functions for tracking vehicles and calculating their speeds.
        - `save_to_csv.py`: Handles saving data to CSV files.
        - `view_transformer.py`: Implements a class for perspective transformation (ViewTransformer). This transforms points from a source view to a target view, useful for aligning camera views to a common perspective.
        - `display.py`:  Provides functions for displaying text and drawing lines on video frames to visualize vehicle counts and directions.
    - `data/`: Stores generated data such as CSV files and captured images.
    - `models/`: Stores YOLOv10 model.
    - `video/`: Stores generated video playlist.
2. Frontend (frontend/):
    - `src/`: Contains the React application code.
    - `components/`: Holds reusable components (e.g., video player, detection results).
    - `App.js` and `index.js`: Set up the main app structure and entry point.
