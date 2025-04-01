import PIL.Image
import pytesseract
import pathlib
import numpy
import cv2


def extract_text(image_path):
    """
    Extract text from an image file with enhanced processing
    optimized for small product packaging images

    Args:
        image_path: Path to the image file

    Returns:
        Extracted text as string
    """
    # Check if path is a file
    image_path_obj = pathlib.Path(image_path)
    if not image_path_obj.is_file():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Read image with OpenCV
    img = cv2.imread(str(image_path_obj))

    if img is None:
        # Try opening with PIL as fallback
        try:
            pil_img = PIL.Image.open(image_path_obj)
            img = numpy.array(pil_img)
            img = img[:, :, ::-1].copy()  # RGB to BGR
        except Exception as e:
            raise ValueError(f"Could not load image: {e}")

    # Get image dimensions
    height, width = img.shape[:2]

    # Resize image if too small (common with product images)
    if width < 800 or height < 800:
        scale_factor = max(3, max(800 / width, 800 / height))
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply binary threshold - this worked best in our tests
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Convert the processed image to PIL format
    img_pil = PIL.Image.fromarray(thresh)

    # Try different Tesseract configurations and combine results
    results = []

    # Default configuration
    default_text = pytesseract.image_to_string(img_pil)
    if default_text.strip():
        results.append(default_text)

    # PSM 11 - sparse text
    custom_config = r"--oem 3 --psm 11"
    sparse_text = pytesseract.image_to_string(img_pil, config=custom_config)
    if sparse_text.strip():
        results.append(sparse_text)

    # Choose the best result or combine them
    if not results:
        return "No text detected in the image."

    # Return the longest result, which likely has the most content
    best_result = max(results, key=lambda x: len(x.strip()))

    return best_result
