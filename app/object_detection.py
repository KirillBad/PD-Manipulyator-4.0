import logging
import os
import traceback
from datetime import datetime

import cv2
import torch
from ultralytics import RTDETR, YOLO
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)


class ObjectDetection:
    def __init__(self):
        try:
            detr_model = RTDETR(os.path.abspath("detr.pt"))
            if torch.cuda.is_available():
                yolo_model = YOLO(os.path.abspath("yolo.engine"), task="detect")
                logger.info("Initializing inference on GPU")
            else:
                yolo_model = YOLO(os.path.abspath("yolo.pt"), task="detect")
                logger.info("Initializing inference on CPU")

            self.models = {"RTDETR": detr_model, "YOLO": yolo_model}
        except Exception as e:
            logger.error(
                f"Failed to initialize models: {str(e)}\n{traceback.format_exc()}"
            )
            raise

        self.input_dir = os.path.join(os.path.dirname(__file__), "media", "input")
        self.output_dir = os.path.join(os.path.dirname(__file__), "media", "output")

    def save_file(self, file):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{file.filename}"
            input_path = os.path.join(self.input_dir, secure_filename(filename))
            file.save(input_path)
            return input_path, filename
        except Exception as e:
            logger.error(f"Failed to save file: {str(e)}\n{traceback.format_exc()}")
            raise

    def handle_video(self, model, file):
        input_path, filename = self.save_file(file)

        return self.process_video(input_path, model)

    def process_video(self, video, model, content_type):
        try:
            if model not in self.models:
                raise ValueError(f"Unknown model: {model}")

            if content_type == "video":
                logger.info(f"Processing video with {model} model")
                video_path = os.path.join(self.input_dir, video)
                if not os.path.exists(video_path):
                    raise FileNotFoundError(f"Video file not found: {video_path}")
                cap = cv2.VideoCapture(video_path)
            else:
                logger.info(f"Processing camera with {model} model")
                cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

            if not cap.isOpened():
                raise RuntimeError("Failed to open video capture")

            selected_model = self.models[model]

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                results = selected_model(frame, stream=True)
                for result in results:
                    processed_frame = result.plot()
                    ret, buffer = cv2.imencode(".jpg", processed_frame)
                    frame_bytes = buffer.tobytes()

                    yield (
                        b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
                    )
                    break

        except Exception as e:
            logger.error(f"Video processing error: {str(e)}\n{traceback.format_exc()}")
            raise
        finally:
            if "cap" in locals():
                cap.release()

    def handle_image(self, model, file):
        try:
            if model not in self.models:
                raise ValueError(f"Unknown model: {model}")

            selected_model = self.models[model]
            input_path, filename = self.save_file(file)

            result = selected_model(input_path)
            handled_result = result[0].plot()
            
            detections_info = []
            for detection in result[0]:
                box = detection.boxes.xyxy[0].tolist() if hasattr(detection.boxes, 'xyxy') else detection.boxes[0].tolist()
                class_id = detection.boxes.cls[0].item()
                class_name = result[0].names[class_id]
                confidence = detection.boxes.conf[0].item()
                
                detections_info.append({
                    "class": class_name,
                    "confidence": float(confidence),
                    "coordinates": {
                        "xmin": float(box[0]),
                        "ymin": float(box[1]),
                        "xmax": float(box[2]),
                        "ymax": float(box[3])
                    }
                })

            print(detections_info)

            output_path = os.path.join(self.output_dir, f"processed_{filename}")
            cv2.imwrite(output_path, handled_result)

            logger.info(
                f"Processed image with {model} in {result[0].speed['inference']} seconds"
            )

            return {"image_path": f"/media/output/processed_{filename}"}
        except Exception as e:
            logger.error(f"Image processing error: {str(e)}\n{traceback.format_exc()}")
            raise


object_detection_handler = ObjectDetection()
