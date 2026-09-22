from pathlib import Path
from datetime import datetime

def generate_report(data: dict, path):
    path = Path(path)
    lines = [
        "VISIONGUARD TRAFFIC ANALYSIS REPORT",
        "=" * 42,
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Source: {data.get('source', '-')}",
        f"Input type: {data.get('type', '-')}",
        "",
        "DETECTION SUMMARY",
        f"Cars: {data.get('cars', 0)}",
        f"Motorcycles: {data.get('motorcycles', 0)}",
        f"Buses: {data.get('buses', 0)}",
        f"Trucks: {data.get('trucks', 0)}",
        f"Bicycles: {data.get('bicycles', 0)}",
        f"Pedestrians: {data.get('pedestrians', 0)}",
        f"Unique tracked objects: {data.get('unique_objects', 0)}",
        f"Traffic density: {data.get('density', '-')}",
        f"Processed frames: {data.get('processed_frames', 0)}",
        f"Source FPS: {data.get('fps', 0.0)}",
        "",
        "NOTE",
        "Density is a heuristic classification based on detected objects per image area.",
        "Results depend on lighting, camera angle, occlusion, video quality and model confidence.",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
