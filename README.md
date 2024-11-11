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
