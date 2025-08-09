# YouTube Slide Detection Tool

## Overview
This tool automatically processes YouTube presentation videos to detect slide changes using OCR (Optical Character Recognition) and outputs timestamps with slide titles. Perfect for analyzing educational content, webinars, and presentation videos.

## Features
- 🎥 **Batch Processing**: Process multiple videos in a directory
- 🔍 **OCR Detection**: Extract slide titles using Tesseract OCR
- ⏱️ **Timestamp Generation**: Accurate timestamps for each slide change
- 📊 **Multiple Output Formats**: JSON, CSV, and text formats
- 🎯 **ROI Support**: Focus OCR on specific screen regions for better accuracy
- 🔧 **Configurable**: Adjustable similarity thresholds and processing intervals

## Installation

### 1. Python Packages
```bash
pip install opencv-python pytesseract Pillow numpy pandas
```

### 2. Tesseract OCR Engine
**Windows:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (tesseract-ocr-w64-setup-5.3.x.exe)
3. Add to PATH or set path manually in code

**Linux (Ubuntu/Debian):**
```bash
sudo apt install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

## Quick Start

### Single Video Processing
```python
from SlideDetector import SlideDetector

# Initialize detector
detector = SlideDetector(
    similarity_threshold=0.7,  # Adjust sensitivity
    frame_interval=3.0         # Check every 3 seconds
)

# Process video
results = detector.process_video(
    video_path="your_video.mp4",
    output_file="results.json"
)

# View results
for slide in results:
    print(f"{slide['timestamp']} - {slide['slide_title']}")
```

### Batch Processing Multiple Videos
```python
from VideoPlaylistProcessor import VideoPlaylistProcessor

# Initialize processor
processor = VideoPlaylistProcessor(similarity_threshold=0.7)

# Process all videos in directory
results = processor.process_playlist(
    directory="path/to/videos",
    output_dir="results"
)
```

## Configuration

### Similarity Threshold
Controls how different slides need to be to register as a change:
- **0.5-0.6**: Very sensitive, detects small changes
- **0.7-0.8**: Balanced, good for most presentations  
- **0.8-0.9**: Less sensitive, only major slide changes

### Frame Interval
How often to check for slide changes:
- **1-2 seconds**: More accurate but slower processing
- **3-5 seconds**: Faster processing, good balance
- **5+ seconds**: Fast but might miss quick slides

### ROI (Region of Interest)
Focus OCR on specific area where slide titles appear:
```python
# Format: (x, y, width, height)
roi = (0, 0, 1920, 300)  # Top 300 pixels of 1920px wide video
detector.process_video(video_path, roi=roi)
```

## Output Formats

### JSON Output
```json
{
  "video_path": "presentation.mp4",
  "total_slides": 15,
  "slides": [
    {
      "timestamp": "00:30",
      "timestamp_seconds": 30.0,
      "slide_title": "Introduction to Machine Learning",
      "full_text": "Introduction to Machine Learning\nChapter 1: Basics"
    }
  ]
}
```

### CSV Output
| timestamp | timestamp_seconds | slide_title | full_text |
|-----------|-------------------|-------------|-----------|
| 00:30     | 30.0             | Introduction | ... |

## Troubleshooting

### Common Issues

**1. "Tesseract not found"**
- Ensure Tesseract is installed and in PATH
- Or set path manually: `pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'`

**2. Poor OCR accuracy**
- Try adjusting the ROI to focus on title area
- Check video quality and resolution
- Experiment with different similarity thresholds

**3. Too many/few slide detections**
- Increase similarity_threshold for fewer detections
- Decrease similarity_threshold for more detections
- Adjust frame_interval based on slide timing

**4. Memory issues with large videos**
- Increase frame_interval to process fewer frames
- Process videos in smaller chunks
- Use ROI to reduce processing area

### Testing OCR Setup
```python
def test_ocr():
    try:
        import pytesseract
        from PIL import Image, ImageDraw
        
        # Create test image
        img = Image.new('RGB', (400, 100), 'white')
        draw = ImageDraw.Draw(img)
        draw.text((10, 30), "Test Slide Title", fill='black')
        
        # Test OCR
        text = pytesseract.image_to_string(img)
        print(f"OCR Result: '{text.strip()}'")
        
        return "Test" in text or "Slide" in text
    except Exception as e:
        print(f"OCR Error: {e}")
        return False

# Run test
if test_ocr():
    print("✅ OCR is working!")
else:
    print("❌ OCR setup needs attention")
```

## Advanced Usage

### Auto-optimize Settings
```python
def find_optimal_settings(video_path):
    best_config = optimize_settings_for_video(video_path)
    print(f"Best settings: {best_config}")
    return best_config
```

### Custom Text Processing
```python
class CustomSlideDetector(SlideDetector):
    def extract_slide_title(self, text):
        # Custom logic for extracting titles
        lines = text.split('\n')
        # Your custom title extraction logic here
        return title
```

## Performance Tips

1. **Use ROI**: Focus on title area to improve speed and accuracy
2. **Adjust frame interval**: Balance between accuracy and speed
3. **Optimize similarity threshold**: Test different values for your content
4. **Batch processing**: Process multiple videos overnight
5. **Pre-process videos**: Ensure good quality and resolution

## File Structure
```
youtube_tools/
├── timestamps_slds.ipynb      # Main notebook with all code
├── requirements.txt           # Python dependencies
├── SLIDE_DETECTION_README.md  # This documentation
└── slide_detection_results/   # Output directory (created automatically)
    ├── video1_timestamps.json
    ├── video2_timestamps.json
    └── all_videos_summary.json
```

## Example Output
For a typical presentation video, you might get:
```
00:30 - Introduction to Data Science
02:15 - What is Machine Learning?
04:45 - Types of Machine Learning
07:20 - Supervised Learning
09:55 - Unsupervised Learning
12:30 - Deep Learning Overview
```

This tool is particularly useful for:
- Creating chapter markers for educational videos
- Analyzing presentation structure
- Generating table of contents for long videos
- Accessibility improvements with slide summaries
- Content indexing and search

## Support
For issues or questions:
1. Check the troubleshooting section
2. Test with a simple video first
3. Verify OCR setup with test function
4. Adjust settings based on your content type

Happy slide detecting! 🎯
