from pathlib import Path
import cv2

TRAFFIC_CLASSES = {
    "car": "cars",
    "motorcycle": "motorcycles",
    "bus": "buses",
    "truck": "trucks",
    "bicycle": "bicycles",
    "person": "pedestrians",
}

class TrafficDetector:
    """YOLO wrapper for traffic-related object detection."""

    def __init__(self, confidence=0.35, model_name="yolo11n.pt"):
        self.confidence = confidence
        self.model_name = model_name
        try:
            from ultralytics import YOLO
            self.model = YOLO(model_name)
        except Exception as exc:
            raise RuntimeError(
                "YOLO model could not be loaded. Install dependencies and allow the first run to download the model."
            ) from exc

    @staticmethod
    def resize_to_width(image, max_width):
        from modules.preprocessing import resize_keep_aspect
        return resize_keep_aspect(image, max_width)

    def detect(self, frame):
        results = self.model.predict(frame, conf=self.confidence, verbose=False)
        result = results[0]
        detections = []

        names = result.names
        if result.boxes is not None:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                label = names[cls_id]
                if label not in TRAFFIC_CLASSES:
                    continue
                xyxy = [int(v) for v in box.xyxy[0].tolist()]
                conf = float(box.conf[0])
                detections.append({
                    "bbox": xyxy,
                    "label": label,
                    "category": TRAFFIC_CLASSES[label],
                    "confidence": conf
                })

        annotated = frame.copy()
        for d in detections:
            x1, y1, x2, y2 = d["bbox"]
            text = f'{d["label"]} {d["confidence"]:.2f}'
            cv2.rectangle(annotated, (x1,y1), (x2,y2), (255,255,255), 2)
            cv2.putText(annotated, text, (x1, max(y1-8, 15)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        return detections, annotated
