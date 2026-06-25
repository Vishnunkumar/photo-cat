"""Configuration constants for the Photo Auto-Categorizer."""

# Supported image file extensions
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}

# YOLOv8 face detection settings
YOLO_MODEL = 'yolov8n.pt'  # Nano model for fast inference
FACE_CONFIDENCE_THRESHOLD = 0.5
IOU_THRESHOLD = 0.45

# Category definitions
CATEGORY_SELFIE = 'Selfie'
CATEGORY_COUPLE = 'Couple'
CATEGORY_GROUP = 'Group'
CATEGORY_OTHER = 'Other'

# Face count thresholds for categories
SELFIE_FACE_COUNT = 1
COUPLE_FACE_COUNT = 2
GROUP_FACE_COUNT_MIN = 5

# Log file name
LOG_FILE_NAME = 'categorizer.log'
