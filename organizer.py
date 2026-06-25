"""File organization module for categorizing photos."""

import shutil
from pathlib import Path
from typing import Optional, Dict
import logging

from config import (
    CATEGORY_SELFIE,
    CATEGORY_COUPLE,
    CATEGORY_GROUP,
    CATEGORY_OTHER,
    SELFIE_FACE_COUNT,
    COUPLE_FACE_COUNT,
    GROUP_FACE_COUNT_MIN
)


class PhotoOrganizer:
    """Organizes photos into categories based on face count."""
    
    def __init__(self, output_dir: Path, dry_run: bool = False):
        """Initialize the photo organizer.
        
        Args:
            output_dir: Directory where categorized photos will be stored.
            dry_run: If True, preview changes without copying files.
        """
        self.output_dir = output_dir
        self.dry_run = dry_run
        self.logger = logging.getLogger(__name__)
        
        # Statistics
        self.stats: Dict[str, int] = {
            'success': 0,
            'skipped': 0,
            'errors': 0
        }
    
    def get_category(self, face_count: int) -> str:
        """Determine category based on face count.
        
        Args:
            face_count: Number of faces detected in the image.
            
        Returns:
            Category name as string.
        """
        if face_count == SELFIE_FACE_COUNT:
            return CATEGORY_SELFIE
        elif face_count == COUPLE_FACE_COUNT:
            return CATEGORY_COUPLE
        elif face_count >= GROUP_FACE_COUNT_MIN:
            return CATEGORY_GROUP
        else:
            return CATEGORY_OTHER
    
    def create_category_directories(self) -> None:
        """Create category subdirectories in the output directory."""
        categories = [CATEGORY_SELFIE, CATEGORY_COUPLE, CATEGORY_GROUP, CATEGORY_OTHER]
        
        for category in categories:
            category_dir = self.output_dir / category
            if not self.dry_run:
                category_dir.mkdir(parents=True, exist_ok=True)
                self.logger.debug(f"Created directory: {category_dir}")
            else:
                self.logger.info(f"[DRY RUN] Would create directory: {category_dir}")
    
    def organize_photo(self, image_path: Path, face_count: int) -> bool:
        """Copy a photo to its category directory.
        
        Args:
            image_path: Path to the source image.
            face_count: Number of faces detected in the image.
            
        Returns:
            True if photo was organized successfully, False otherwise.
        """
        category = self.get_category(face_count)
        category_dir = self.output_dir / category
        destination = category_dir / image_path.name
        
        # Check if destination already exists
        if destination.exists():
            self.logger.warning(f"Skipping {image_path.name}: destination already exists")
            self.stats['skipped'] += 1
            return False
        
        try:
            if not self.dry_run:
                shutil.copy2(image_path, destination)
                self.logger.info(f"Copied {image_path.name} to {category}/")
            else:
                self.logger.info(f"[DRY RUN] Would copy {image_path.name} to {category}/")
            
            self.stats['success'] += 1
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to copy {image_path.name}: {e}")
            self.stats['errors'] += 1
            return False
    
    def get_statistics(self) -> Dict[str, int]:
        """Get organization statistics.
        
        Returns:
            Dictionary with success, skipped, and error counts.
        """
        return self.stats.copy()
