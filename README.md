# 🚦 VisionGuard

**Intelligent Traffic Detection, Tracking & Density Analysis using Computer Vision**

VisionGuard is an academic Computer Vision project that analyzes road images and videos using **YOLO, OpenCV and Python**. It detects common traffic objects, tracks detections across video frames, counts categories, estimates traffic density, and generates a downloadable report.

## Features

- 🖼️ Image analysis
- 🎥 Video analysis
- 🎯 YOLO object detection
- 🔄 Centroid-based object tracking
- 🚗 Vehicle and pedestrian counting
- 📊 Traffic-density classification
- 📹 Annotated output video
- 📄 Downloadable analysis report
- ⚠️ Input validation and error handling
- 🧪 Unit tests

## Computer Vision Concepts

- Image/video acquisition
- Image resizing and preprocessing
- Object detection
- Bounding boxes and confidence scores
- Object tracking
- Object counting
- Density estimation
- Visual annotation
- Performance statistics

## Technology Stack

- Python
- OpenCV
- Ultralytics YOLO
- Streamlit
- NumPy
- Pandas
- PyTest

## Project Structure

```text
VisionGuard/
├── app.py
├── modules/
│   ├── detector.py
│   ├── tracker.py
│   ├── counter.py
│   ├── density.py
│   ├── preprocessing.py
│   └── report.py
├── utils/
│   ├── config.py
│   └── helpers.py
├── tests/
│   └── test_core.py
├── assets/
├── outputs/
├── requirements.txt
├── statement.md
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/VisionGuard.git
cd VisionGuard
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

On the first analysis, the Ultralytics model may download its model weights automatically. Internet access is therefore required for the first model setup unless the model weights are already available locally.

## Testing

Run:

```bash
pytest -q
```

The tests cover input validation, density classification and counting logic.

## How to Use

1. Start the Streamlit application.
2. Upload a road image or video.
3. Select the detection confidence.
4. Select the processing interval.
5. Click **Analyse Traffic**.
6. View the annotated result and traffic statistics.
7. Download the processed video/report when available.

## Limitations

- Detection accuracy depends on the pretrained YOLO model and scene conditions.
- The tracker is a lightweight centroid tracker rather than a production-grade tracking algorithm.
- Density is a heuristic based on detected objects per image area.
- Severe occlusion, poor lighting, unusual camera angles and low-resolution footage can reduce accuracy.
- The system is an academic prototype, not a certified traffic-enforcement system.

## Future Enhancements

- Helmet detection
- Number-plate recognition
- Lane detection
- Red-light violation detection
- Accident detection
- Heat-map generation
- Database-backed analysis history
- Real-time CCTV integration
- Cloud deployment

## License

This repository is intended for academic/educational use. Check the licenses of third-party models and libraries before redistributing model weights or deploying the system commercially.
