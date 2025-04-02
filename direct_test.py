#!/usr/bin/env python3
import cv2
import subprocess
import os
import PIL.Image
import PIL.ImageEnhance
import argparse


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Test OCR capabilities on an image")
    parser.add_argument("image", help="Path to the image file")
    parser.add_argument(
        "--scale", type=int, default=3, help="Scale factor for resizing"
    )
    parser.add_argument(
        "--contrast", type=float, default=2.0, help="Contrast enhancement factor"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed output"
    )
    return parser.parse_args()


def main():
    """Main function"""
    args = parse_arguments()
    image_path = args.image
    scale_factor = args.scale
    contrast_factor = args.contrast

    print(f"Testing OCR on {image_path}")
    print(f"Image size: {os.path.getsize(image_path)} bytes")

    # First, try direct tesseract
    print("\n=== Direct tesseract output ===")
    subprocess.run(["tesseract", image_path, "stdout"])

    # Load the image with OpenCV
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    print(f"\nOriginal dimensions: {width}x{height}")

    # Resize to larger
    resized = cv2.resize(
        img,
        (width * scale_factor, height * scale_factor),
        interpolation=cv2.INTER_CUBIC,
    )
    resized_path = "resized_image.jpg"
    cv2.imwrite(resized_path, resized)
    print(f"Resized to: {width * scale_factor}x{height * scale_factor}")

    # Try tesseract on resized image
    print("\n=== Tesseract on resized image ===")
    subprocess.run(["tesseract", resized_path, "stdout"])

    # Try different preprocessing techniques
    # 1. Grayscale
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    gray_path = "gray_image.jpg"
    cv2.imwrite(gray_path, gray)

    # 2. Threshold
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    thresh_path = "thresh_image.jpg"
    cv2.imwrite(thresh_path, thresh)

    # 3. Adaptive threshold
    adaptive = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    adaptive_path = "adaptive_image.jpg"
    cv2.imwrite(adaptive_path, adaptive)

    # Try OCR on preprocessed images
    print("\n=== Tesseract on grayscale image ===")
    subprocess.run(["tesseract", gray_path, "stdout"])
    print("\n=== Tesseract on threshold image ===")
    subprocess.run(["tesseract", thresh_path, "stdout"])
    print("\n=== Tesseract on adaptive threshold image ===")
    subprocess.run(["tesseract", adaptive_path, "stdout"])

    # Try PIL enhancement
    pil_img = PIL.Image.open(image_path)
    # Resize
    pil_resized = pil_img.resize(
        (width * scale_factor, height * scale_factor), PIL.Image.LANCZOS
    )
    # Enhance contrast
    enhancer = PIL.ImageEnhance.Contrast(pil_resized)
    enhanced = enhancer.enhance(contrast_factor)  # Increase contrast
    enhanced_path = "enhanced_image.jpg"
    enhanced.save(enhanced_path)
    print("\n=== Tesseract on PIL enhanced image ===")
    subprocess.run(["tesseract", enhanced_path, "stdout"])

    # Try different Tesseract configs
    print("\n=== Tesseract with different PSM modes ===")
    for psm in [3, 4, 6, 11, 12]:
        print(f"\nPSM mode {psm}:")
        subprocess.run(["tesseract", enhanced_path, "stdout", "--psm", str(psm)])


if __name__ == "__main__":
    main()
