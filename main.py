"""Main entry point for the Photo Auto-Categorizer CLI."""

import argparse
import sys
import time
from pathlib import Path
from typing import Optional

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

from detector import FaceDetector
from organizer import PhotoOrganizer
from utils import (
    validate_input_directory,
    validate_output_directory,
    get_image_files,
    setup_logging
)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.
    
    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description='Photo Auto-Categorizer - Organize photos by face count using YOLOv8n',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --input_dir "C:\\Users\\user\\Pictures" --output_dir "D:\\Organized"
  python main.py --input_dir "./photos" --output_dir "./organized" --loglevel DEBUG
  python main.py --input_dir "./photos" --output_dir "./organized" --dry-run
        """
    )
    
    parser.add_argument(
        '--input_dir',
        type=str,
        required=True,
        help='Source directory containing photos to categorize'
    )
    
    parser.add_argument(
        '--output_dir',
        type=str,
        required=True,
        help='Destination directory for categorized photos'
    )
    
    parser.add_argument(
        '--loglevel',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level (default: INFO)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without copying files'
    )
    
    return parser.parse_args()


def main() -> int:
    """Main execution function.
    
    Returns:
        Exit code (0 for success, 1 for failure).
    """
    args = parse_arguments()
    
    # Convert paths to Path objects
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    
    # Validate input directory
    if not validate_input_directory(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist or is not readable.")
        return 1
    
    # Validate output directory
    if not validate_output_directory(output_dir):
        print(f"Error: Output directory '{output_dir}' cannot be created or is not writable.")
        return 1
    
    # Create output directory if it doesn't exist
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Setup logging
    logger = setup_logging(args.loglevel, output_dir)
    logger.info("Photo Auto-Categorizer started")
    logger.info(f"Input directory: {input_dir}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Log level: {args.loglevel}")
    logger.info(f"Dry run: {args.dry_run}")
    
    # Get all image files
    logger.info("Scanning for image files...")
    image_files = get_image_files(input_dir)
    
    if not image_files:
        logger.warning("No valid image files found in input directory")
        return 0
    
    logger.info(f"Found {len(image_files)} image file(s)")
    
    # Initialize face detector
    try:
        detector = FaceDetector()
        logger.info("YOLOv8n face detector initialized")
    except Exception as e:
        logger.error(f"Failed to initialize face detector: {e}")
        return 1
    
    # Initialize organizer
    organizer = PhotoOrganizer(output_dir, dry_run=args.dry_run)
    
    # Create category directories
    organizer.create_category_directories()
    
    # Process images
    start_time = time.time()
    logger.info("Processing images...")
    
    # Use tqdm if available, otherwise simple iteration
    iterator = tqdm(image_files, desc="Processing") if tqdm else image_files
    
    for image_path in iterator:
        logger.debug(f"Processing: {image_path.name}")
        
        # Validate image
        if not detector.validate_image(image_path):
            logger.warning(f"Skipping invalid image: {image_path.name}")
            organizer.stats['skipped'] += 1
            continue
        
        # Detect faces
        try:
            face_count = detector.detect_faces(image_path)
        except Exception as e:
            logger.error(f"Failed to detect faces in {image_path.name}: {e}")
            organizer.stats['errors'] += 1
            continue
        
        # Organize photo
        organizer.organize_photo(image_path, face_count)
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    
    # Print statistics
    stats = organizer.get_statistics()
    logger.info("=" * 50)
    logger.info("Processing complete")
    logger.info(f"Total time: {elapsed_time:.2f} seconds")
    logger.info(f"Success: {stats['success']}")
    logger.info(f"Skipped: {stats['skipped']}")
    logger.info(f"Errors: {stats['errors']}")
    logger.info("=" * 50)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
