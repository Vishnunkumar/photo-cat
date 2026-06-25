# Photo Auto-Categorizer CLI

A Python CLI tool that automatically organizes photos into categories based on the number of faces detected in each image.

## Features

- **Automatic Face Detection**: Uses YOLOv8n for fast, accurate person detection (no GPU required)
- **Smart Categorization**: Organizes photos into four categories:
  - **Selfie**: Exactly 1 person detected
  - **Couple**: Exactly 2 people detected
  - **Group**: 5 or more people detected
  - **Other**: Photos with 3-4 people or non-categorizable images
- **Safe Processing**: Copies files (doesn't move) to preserve originals
- **Comprehensive Logging**: Logs all operations to both console and file
- **Dry Run Mode**: Preview changes before actual file operations
- **Progress Tracking**: Optional progress bar for large batches
- **Windows Friendly**: Handles Windows paths and UNC paths correctly

## Requirements

- Python 3.8 or higher (tested on Python 3.14)
- Windows, macOS, or Linux

## Installation

1. Clone or download this repository
2. Navigate to the `photo_categorizer` directory
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python main.py --input_dir "C:\Users\user\Pictures" --output_dir "D:\Organized"
```

### With Custom Log Level

```bash
python main.py --input_dir "./photos" --output_dir "./organized" --loglevel DEBUG
```

### Dry Run (Preview Without Copying)

```bash
python main.py --input_dir "./photos" --output_dir "./organized" --dry-run
```

### Command-Line Arguments

- `--input_dir` (required): Source directory containing photos to categorize
- `--output_dir` (required): Destination directory for categorized photos
- `--loglevel` (optional): Logging level - DEBUG, INFO, WARNING, or ERROR (default: INFO)
- `--dry-run` (optional): Preview changes without copying files

### Help

```bash
python main.py --help
```

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- WebP (.webp)
- TIFF (.tiff, .tif)

## Output Structure

The tool creates the following directory structure in the output directory:

```
output_dir/
├── Selfie/      # Photos with exactly 1 face
├── Couple/      # Photos with exactly 2 faces
├── Group/       # Photos with 5 or more faces
├── Other/       # Photos with 3-4 faces or non-categorizable
└── categorizer.log  # Log file with detailed operation history
```

## Logging

Logs are written to both:
- **Console**: Real-time progress and status updates
- **File**: `categorizer.log` in the output directory with complete operation history

Log format: `[TIMESTAMP] [LEVEL] [filename] - message`

## Error Handling

The tool handles various error conditions gracefully:
- Invalid or corrupted images are skipped with a warning
- Permission errors are logged without crashing
- File conflicts (duplicate filenames) are skipped with a warning
- Processing continues for remaining files even if individual files fail

## Performance

- Processes images sequentially to avoid memory overload
- Logs total processing time at completion
- Skips non-image files silently
- Uses YOLOv8n nano model for fast CPU inference (no GPU required)

## Technical Details

### Face Detection

- **Library**: Ultralytics YOLOv8
- **Model**: YOLOv8n (nano model for fast inference)
- **Detection**: Person detection using COCO dataset (class 0)
- **Confidence Threshold**: 0.5 (configurable in `config.py`)
- **IoU Threshold**: 0.45 (configurable in `config.py`)
- **Performance**: Optimized for CPU, no GPU required

### File Operations

- **Operation**: Copy (preserves originals)
- **Conflict Handling**: Skip if destination exists
- **Metadata**: Preserves file modification timestamps

## Example Output

```
[2024-06-25 12:00:00] [INFO] [main.py] - Photo Auto-Categorizer started
[2024-06-25 12:00:00] [INFO] [main.py] - Input directory: C:\Users\user\Pictures
[2024-06-25 12:00:00] [INFO] [main.py] - Output directory: D:\Organized
[2024-06-25 12:00:00] [INFO] [main.py] - Found 150 image file(s)
[2024-06-25 12:00:00] [INFO] [main.py] - Processing images...
Processing: 100%|████████████████████| 150/150 [02:30<00:00, 1.00s/it]
[2024-06-25 12:02:30] [INFO] [main.py] - ==================================================
[2024-06-25 12:02:30] [INFO] [main.py] - Processing complete
[2024-06-25 12:02:30] [INFO] [main.py] - Total time: 150.00 seconds
[2024-06-25 12:02:30] [INFO] [main.py] - Success: 145
[2024-06-25 12:02:30] [INFO] [main.py] - Skipped: 3
[2024-06-25 12:02:30] [INFO] [main.py] - Errors: 2
[2024-06-25 12:02:30] [INFO] [main.py] - ==================================================
```

## Troubleshooting

### "No valid image files found"
- Ensure the input directory contains supported image formats (.jpg, .jpeg, .png, .gif, .bmp, .webp, .tiff, .tif)
- Check that you have read permissions for the input directory

### "Failed to initialize face detector"
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- The YOLOv8n model will be automatically downloaded on first run
- Check your internet connection for the initial model download

### "Output directory cannot be created"
- Ensure you have write permissions for the parent directory
- Check that the path is valid on your operating system

## License

This project is provided as-is for personal and educational use.

## Dependencies

- **ultralytics**: YOLOv8 object detection library
- **Pillow**: Image validation
- **tqdm**: Progress bar (optional but recommended)
