import cv2
import numpy
import pytesseract
import PIL.Image
import pathlib


def preprocess_image(image):
    """
    Preprocess the image to improve OCR results
    Args:
        image: Image loaded with OpenCV
    Returns:
        Preprocessed image
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply threshold to get black and white image
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Optional: noise removal
    kernel = numpy.ones((1, 1), numpy.uint8)
    img_processed = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    return img_processed


def extract_text(image_path):
    """
    Extract text from an image file
    Args:
        image_path: Path to the image file
    Returns:
        Extracted text as string
    """
    # Check if file exists
    image_path_obj = pathlib.Path(image_path)
    if not image_path_obj.is_file():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Load image with OpenCV
    img = cv2.imread(str(image_path_obj))
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")

    # Preprocess the image
    img_processed = preprocess_image(img)

    # Convert the OpenCV image to PIL format for pytesseract
    img_pil = PIL.Image.fromarray(img_processed)

    # Extract text
    text = pytesseract.image_to_string(img_pil)
    return text
