import streamlit as st
from pathlib import Path
import tempfile
import cv2
import pandas as pd

from modules.preprocessing import validate_media, save_uploaded_file
from modules.detector import TrafficDetector
from modules.tracker import CentroidTracker
from modules.counter import VehicleCounter
from modules.density import DensityAnalyzer
from modules.report import generate_report

st.set_page_config(page_title="VisionGuard", page_icon="🚦", layout="wide")

st.title("🚦 VisionGuard")
st.caption("Computer-vision based traffic detection, counting and density analysis")

with st.sidebar:
    st.header("Settings")
    confidence = st.slider("Detection confidence", 0.10, 0.95, 0.35, 0.05)
    process_every = st.slider("Process every Nth frame", 1, 5, 1)
    max_width = st.slider("Processing width", 480, 1280, 960, 80)

uploaded = st.file_uploader(
    "Upload a road image or video",
    type=["jpg", "jpeg", "png", "mp4", "avi", "mov", "mkv"]
)

if uploaded:
    ok, message, kind = validate_media(uploaded.name)
    if not ok:
        st.error(message)
        st.stop()

    work_dir = Path(tempfile.mkdtemp(prefix="visionguard_"))
    input_path = save_uploaded_file(uploaded, work_dir)

    if "analyze" not in st.session_state:
        st.session_state.analyze = False

    if st.button("🔎 Analyse Traffic", type="primary"):
        st.session_state.analyze = True

    if st.session_state.analyze:
        try:
            detector = TrafficDetector(confidence=confidence)
            tracker = CentroidTracker()
            counter = VehicleCounter()
            density = DensityAnalyzer()
            report_data = {
                "source": uploaded.name,
                "type": kind,
                "cars": 0,
                "motorcycles": 0,
                "buses": 0,
                "trucks": 0,
                "bicycles": 0,
                "pedestrians": 0,
                "unique_objects": 0,
                "density": "LOW",
                "processed_frames": 0,
                "fps": 0.0,
            }

            if kind == "image":
                image = cv2.imread(str(input_path))
                if image is None:
                    st.error("The image could not be decoded.")
                    st.stop()

                image = detector.resize_to_width(image, max_width)
                detections, annotated = detector.detect(image)
                tracks = tracker.update(detections)
                counter.update(tracks)
                counts = counter.count_by_class(tracks)
                report_data.update(counts)
                report_data["unique_objects"] = len(counter.seen_ids)
                report_data["density"] = density.classify(len(tracks), image.shape[1], image.shape[0])
                report_data["processed_frames"] = 1

                c1, c2 = st.columns([2, 1])
                with c1:
                    st.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), caption="Processed image", use_container_width=True)
                with c2:
                    st.subheader("Traffic Summary")
                    st.metric("Vehicles", sum(counts[k] for k in ["cars","motorcycles","buses","trucks","bicycles"]))
                    st.metric("Pedestrians", counts["pedestrians"])
                    st.metric("Density", report_data["density"])
                    st.write(counts)

            else:
                cap = cv2.VideoCapture(str(input_path))
                if not cap.isOpened():
                    st.error("The video could not be opened.")
                    st.stop()

                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
                source_fps = float(cap.get(cv2.CAP_PROP_FPS) or 0)
                writer = None
                output_path = work_dir / "visionguard_output.mp4"
                frame_placeholder = st.empty()
                progress = st.progress(0)
                frame_index = 0
                processed = 0

                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    frame_index += 1
                    if frame_index % process_every != 0:
                        continue

                    frame = detector.resize_to_width(frame, max_width)
                    detections, annotated = detector.detect(frame)
                    tracks = tracker.update(detections)
                    counter.update(tracks)
                    counts = counter.count_by_class(tracks)
                    current_density = density.classify(len(tracks), frame.shape[1], frame.shape[0])

                    if writer is None:
                        h, w = annotated.shape[:2]
                        writer = cv2.VideoWriter(
                            str(output_path),
                            cv2.VideoWriter_fourcc(*"mp4v"),
                            max(source_fps / process_every, 1),
                            (w, h)
                        )
                    writer.write(annotated)
                    frame_placeholder.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)
                    processed += 1
                    if total_frames:
                        progress.progress(min(frame_index / total_frames, 1.0))

                cap.release()
                if writer:
                    writer.release()

                counts = counter.count_by_class(tracker.active_tracks)
                report_data.update(counts)
                report_data["unique_objects"] = len(counter.seen_ids)
                report_data["density"] = density.classify(len(tracker.active_tracks), max_width, max_width * 0.56)
                report_data["processed_frames"] = processed
                report_data["fps"] = source_fps

                st.subheader("Traffic Summary")
                cols = st.columns(4)
                cols[0].metric("Vehicles", sum(counts[k] for k in ["cars","motorcycles","buses","trucks","bicycles"]))
                cols[1].metric("Pedestrians", counts["pedestrians"])
                cols[2].metric("Unique tracked", len(counter.seen_ids))
                cols[3].metric("Density", report_data["density"])

                if output_path.exists():
                    with open(output_path, "rb") as f:
                        st.download_button("⬇️ Download processed video", f, file_name="visionguard_output.mp4", mime="video/mp4")

            st.subheader("Detailed Results")
            df = pd.DataFrame([report_data])
            st.dataframe(df, use_container_width=True)

            report_path = generate_report(report_data, work_dir / "VisionGuard_Report.txt")
            with open(report_path, "rb") as f:
                st.download_button("📄 Download analysis report", f, file_name="VisionGuard_Report.txt", mime="text/plain")

        except Exception as exc:
            st.error(f"Analysis failed: {exc}")
else:
    st.info("Upload an image or video to begin.")
    st.markdown("""
    ### What VisionGuard does
    - Detects road objects with YOLO
    - Tracks detected objects across video frames
    - Counts object categories
    - Classifies traffic density
    - Produces processed media and a text report
    """)
