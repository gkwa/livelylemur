# Import extract_text lazily to avoid immediate dependency errors
def extract_text(image_path):
    """
    Extract text from an image file

    Args:
        image_path: Path to the image file

    Returns:
        Extracted text as string
    """
    try:
        from .ocr import extract_text as ocr_extract_text

        return ocr_extract_text(image_path)
    except ImportError as e:
        if "libGL.so.1" in str(e):
            raise ImportError(
                "OpenCV system libraries are missing. Install them with:\n"
                "  Ubuntu/Debian: sudo apt-get install libgl1-mesa-glx\n"
                "  CentOS/RHEL: sudo yum install mesa-libGL\n"
                "  Amazon Linux: sudo yum install mesa-libGL\n\n"
                "Or use the fallback mode by importing from livelylemur.fallback"
            ) from e
        raise


# Expose main function from cli module
from .cli import main
