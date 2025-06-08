# Image Storage System

This document describes how the image storage system works in this application.

## Overview

Images are stored in two places:
1. **Filesystem**: In the `app/static/uploads` directory
2. **Database**: In the `image_storage` table as binary data

This dual storage approach provides redundancy and ensures images aren't lost when deploying or during git operations.

## Features

- **Redundant Storage**: Images are saved both to the filesystem and database
- **Absolute Path Handling**: Fixed path issues that previously caused upload failures
- **UUID Filenames**: Most uploads use UUID-based filenames to prevent collisions
- **Automatic Directory Creation**: Uploads directory is created if missing
- **Image Restoration**: Missing files can be restored from database backups

## Tools

Several utility scripts are provided:

### 1. migrate_images.py

Creates the ImageStorage table and migrates existing filesystem images to the database.

```
python app/migrate_images.py
```

### 2. test_image_storage.py

Tests if images are properly backed up in the database and checks restoration functionality.

```
python app/test_image_storage.py
```

### 3. restore_images.py

Restores any missing images from the database backup.

```
python app/restore_images.py
```

## How It Works

1. When an image is uploaded, it's saved to the filesystem using `save_uploaded_file()` 
2. The image is also saved to the database via `ImageStorage.store_image()`
3. If an image is missing from the filesystem (e.g., after git pull), it can be restored from the database

## Deployment Considerations

After deploying:

1. Run the `restore_images.py` script to make sure all images are present in the filesystem
2. Periodically backup the database to ensure image data is preserved

## Troubleshooting

If images aren't showing up:

1. Check if the file exists in the `app/static/uploads` directory
2. Run `python app/restore_images.py` to restore any missing files
3. Check the database to ensure images are being backed up properly
4. Ensure proper file permissions on the uploads directory
