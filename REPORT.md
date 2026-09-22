# VisionGuard — Project Report

## 1. Cover Page

**Project Title:** VisionGuard — Intelligent Traffic Detection, Tracking & Density Analysis  
**Subject:** Computer Vision  
**Student:** __________________________  
**Registration Number:** __________________________  
**Faculty:** __________________________  
**Institution:** __________________________  
**Academic Year:** 2026–27

---

## 2. Introduction

Computer Vision enables computers to extract useful information from images and videos. Traffic scenes contain multiple visual objects such as cars, motorcycles, buses, trucks, bicycles and pedestrians. Automatically identifying these objects can help convert raw visual footage into structured information.

VisionGuard is an academic prototype that applies object detection, tracking, counting and density analysis to road images and videos.

---

## 3. Problem Statement

Manual traffic observation requires continuous human attention and does not scale efficiently. VisionGuard addresses this problem by processing visual traffic data and automatically extracting object-level statistics.

---

## 4. Objectives

1. Detect common road objects from images and videos.
2. Track detected objects across video frames.
3. Count traffic-object categories.
4. Estimate traffic density using a transparent heuristic.
5. Provide visual annotations and a downloadable report.
6. Demonstrate modular Computer Vision implementation.

---

## 5. Functional Requirements

### FR1 — Media Input
The user shall upload a supported road image or video.

### FR2 — Object Detection
The system shall detect supported traffic-related classes and display bounding boxes with confidence scores.

### FR3 — Object Tracking
For video input, the system shall assign lightweight tracking IDs to detections across frames.

### FR4 — Counting
The system shall calculate category-level object counts.

### FR5 — Density Analysis
The system shall classify the current scene as LOW, MEDIUM or HIGH using detected objects relative to image area.

### FR6 — Reporting
The system shall generate a text analysis report containing detection and processing statistics.

---

## 6. Non-Functional Requirements

### Performance
The system should process frames efficiently and expose a configurable frame-processing interval.

### Usability
The Streamlit interface should allow analysis without requiring command-line interaction after startup.

### Reliability
Unsupported media and decoding/model errors should be handled with user-visible messages.

### Maintainability
Detection, tracking, counting, density analysis and reporting are implemented as separate modules.

### Resource Efficiency
The application supports configurable processing width and frame interval.

### Error Handling
Input validation and exception handling should prevent common failures from terminating the interface without explanation.

---

## 7. System Architecture

```text
+----------------+
|      User      |
+-------+--------+
        |
        v
+----------------------+
| Streamlit Input UI   |
| Image / Video        |
+----------+-----------+
           |
           v
+----------------------+
| Preprocessing        |
| Validation / Resize  |
+----------+-----------+
           |
           v
+----------------------+
| YOLO Object Detector |
+----------+-----------+
           |
           v
+----------------------+
| Centroid Tracker     |
+----------+-----------+
           |
           v
+----------------------+
| Counter              |
+----------+-----------+
           |
           v
+----------------------+
| Density Analyzer     |
+----------+-----------+
           |
           v
+----------------------+
| Visualization +      |
| Report Generator     |
+----------------------+
```

---

## 8. Workflow Diagram

```text
START
  |
  v
Upload Media
  |
  v
Validate Format
  |
  +---- Invalid ----> Display Error ----> END
  |
 Valid
  |
  v
Preprocess / Resize
  |
  v
Run Object Detection
  |
  v
Track Objects (video)
  |
  v
Count Categories
  |
  v
Estimate Density
  |
  v
Display Results
  |
  v
Generate Report
  |
  v
END
```

---

## 9. Use Case Diagram

```text
                 +------------------+
                 |       User       |
                 +--------+---------+
                          |
          +---------------+----------------+
          |               |                |
          v               v                v
     Upload Media    Analyse Traffic   Download Report
                          |
                    +-----+------+
                    |            |
                    v            v
              Detect Objects  Track Objects
                    |
                    v
                 Count
                    |
                    v
              Analyse Density
```

### Primary Actor
User

### Use Cases
- Upload media
- Analyse traffic
- View detection results
- View counts
- View density
- Download report

---

## 10. Component/Class Design

```text
+-----------------------+
| TrafficDetector       |
+-----------------------+
| confidence            |
| model                 |
+-----------------------+
| detect()              |
| resize_to_width()     |
+-----------------------+

+-----------------------+
| CentroidTracker       |
+-----------------------+
| tracks                |
| next_id               |
+-----------------------+
| update()              |
| centroid()            |
+-----------------------+

+-----------------------+
| VehicleCounter        |
+-----------------------+
| seen_ids              |
| latest_counts         |
+-----------------------+
| update()              |
| count_by_class()      |
+-----------------------+

+-----------------------+
| DensityAnalyzer       |
+-----------------------+
| low                   |
| medium                |
+-----------------------+
| classify()            |
| score()               |
+-----------------------+

+-----------------------+
| ReportGenerator       |
+-----------------------+
| generate_report()     |
+-----------------------+
```

---

## 11. Sequence Diagram

```text
User       UI       Detector      Tracker      Counter      Density
 |          |           |             |            |            |
 | Upload   |           |             |            |            |
 |--------->|           |             |            |            |
 |          | Detect    |             |            |            |
 |          |---------->|             |            |            |
 |          |<----------| detections  |            |            |
 |          | Track     |             |            |            |
 |          |------------------------>|            |            |
 |          |<------------------------| tracks     |            |
 |          | Count                                  |          |
 |          |--------------------------------------->|          |
 |          |<---------------------------------------| counts   |
 |          | Density                                             |
 |          |---------------------------------------------------->|
 |          |<----------------------------------------------------|
 |<---------| Results                                             |
```

---

## 12. Database/Storage Design

The baseline project does not require a persistent database. Uploaded files are processed in temporary working directories and the user can download the resulting report/media.

If a database is added later, an `Analysis` table can store:

```text
Analysis
---------
analysis_id
timestamp
source_file
cars
motorcycles
buses
trucks
bicycles
pedestrians
unique_objects
density
processed_frames
fps
```

---

## 13. Design Decisions & Rationale

### YOLO
A pretrained object detector is used so that the project can demonstrate practical object detection without requiring a large custom training dataset.

### OpenCV
OpenCV provides image/video decoding, resizing and visual annotation.

### Centroid Tracking
A lightweight centroid tracker keeps the implementation understandable and demonstrates the concept of temporal object association.

### Streamlit
Streamlit provides a simple browser-based interface suitable for an academic demonstration.

### Modular Architecture
Separate modules make the implementation easier to test, explain and maintain.

---

## 14. Implementation Details

### Detection
The detector uses a pretrained YOLO model. Each detection provides a bounding box, class label and confidence score. Only selected traffic-related classes are retained.

### Tracking
Each detected object's bounding-box centroid is compared with existing track centroids. A nearest same-class detection within a configurable distance is associated with the existing ID.

### Counting
The counter records active category counts and maintains a set of IDs observed during the video.

### Density
Density is calculated using:

`density_score = detected_objects / image_area`

The score is mapped to LOW, MEDIUM or HIGH using configurable thresholds.

### Reporting
The report generator writes source information, category counts, unique tracked objects, density, processed frames and FPS to a text report.

---

## 15. Screenshots / Results

Add screenshots after running the project:

1. Application home page
2. Image detection result
3. Video detection result
4. Traffic summary
5. Download report

Suggested GitHub/report captions:

- **Figure 1:** VisionGuard home interface
- **Figure 2:** Object detection with bounding boxes
- **Figure 3:** Traffic category statistics
- **Figure 4:** Processed video output

---

## 16. Testing Approach

Unit tests are included for:

- Media-extension validation
- Density classification
- Category counting

Run:

```bash
pytest -q
```

### Example test cases

| Test | Input | Expected |
|---|---|---|
| Valid image | road.jpg | Accepted |
| Valid video | traffic.mp4 | Accepted |
| Invalid file | file.exe | Rejected |
| Zero detections | 0 objects | LOW |
| Category count | 2 cars + 1 person | Cars=2, pedestrians=1 |

---

## 17. Challenges Faced

- Managing different image and video input formats
- Balancing processing speed and detection quality
- Maintaining object IDs across video frames
- Handling model-loading and media-decoding failures
- Designing a simple density metric that can be explained clearly

---

## 18. Learnings & Key Takeaways

- Practical use of object detection in Computer Vision
- Working with image and video frames using OpenCV
- Understanding bounding boxes and confidence scores
- Basic object tracking and temporal association
- Modular Python project design
- Input validation and error handling
- Building a user-facing Computer Vision application
- Using Git/GitHub for version control

---

## 19. Future Enhancements

- Helmet detection
- Number-plate recognition
- Lane detection
- Traffic-light state recognition
- Red-light violation detection
- Accident detection
- Heat-map visualization
- Persistent database and analysis history
- Real-time CCTV integration
- Cloud deployment

---

## 20. References

1. OpenCV Documentation — https://docs.opencv.org/
2. Ultralytics Documentation — https://docs.ultralytics.com/
3. Streamlit Documentation — https://docs.streamlit.io/
4. Python Documentation — https://docs.python.org/3/
5. PyTest Documentation — https://docs.pytest.org/

---

## 21. Conclusion

VisionGuard demonstrates how Computer Vision can transform road images and videos into structured traffic information. The modular architecture combines object detection, tracking, counting, density analysis and reporting into one academic application. The project provides a practical demonstration of Computer Vision concepts while leaving clear opportunities for future extensions.
