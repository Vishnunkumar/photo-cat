"""Face detection module using YOLOv8n."""

import logging
from pathlib import Path
from typing import Optional

from PIL import Image
from ultralytics import YOLO

from config import (
    YOLO_MODEL,
    FACE_CONFIDENCE_THRESHOLD,
    IOU_THRESHOLD
)


class FaceDetector:
    """Face detector using YOLOv8n model."""
    
    def __init__(
        self,
        model_name: str = YOLO_MODEL,
        confidence_threshold: float = FACE_CONFIDENCE_THRESHOLD,
        iou_threshold: float = IOU_THRESHOLD
    ):
        """Initialize the face detector.
        
        Args:
            model_name: YOLO model to use (default: yolov8n.pt).
            confidence_threshold: Minimum confidence score for face detection.
            iou_threshold: IoU threshold for NMS.
        """
        self.model_name = model_name
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        self.logger = logging.getLogger(__name__)
        self._initialize_detector()
    
    def _initialize_detector(self) -> None:
        """Initialize YOLOv8 face detection model."""
        try:
            # Load YOLOv8n model (will download if not present)
            self.model = YOLO(self.model_name)
            self.logger.debug(f"YOLOv8 model '{self.model_name}' initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize YOLO model: {e}")
            raise
    
    def detect_faces(self, image_path: Path) -> int:
        """Detect faces in an image file using YOLOv8.
        
        Args:
            image_path: Path to the image file.
            
        Returns:
            Number of faces detected in the image.
            
        Raises:
            Exception: If image cannot be processed.
        """
        try:
            # Run inference
            results = self.model(
                str(image_path),
                conf=self.confidence_threshold,
                iou=self.iou_threshold,
                verbose=False
            )
            
            # Count faces (class 0 is 'person' in COCO dataset)
            face_count = 0
            for result in results:
                # Filter for person class (class 0 in COCO)
                person_detections = [
                    box for box in result.boxes 
                    if box.cls == 0 and box.conf >= self.confidence_threshold
                ]
                face_count = len(person_detections)
            
            self.logger.debug(f"Detected {face_count} face(s) in {image_path.name}")
            return face_count
            
        except Exception as e:
            self.logger.error(f"Error processing image {image_path}: {e}")
            raise
    
    def validate_image(self, image_path: Path) -> bool:
        """Validate that a file is a readable image.
        
        Args:
            image_path: Path to the image file.
            
        Returns:
            True if the file is a valid image, False otherwise.
        """
        try:
            with Image.open(image_path) as img:
                img.verify()
            return True
        except Exception as e:
            self.logger.warning(f"Invalid image file {image_path}: {e}")
            return False
