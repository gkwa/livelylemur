import argparse
import sys
import pathlib
import tempfile
import re
import urllib.request


def is_url(text):
    """
    Check if a string is a URL

    Args:
        text: String to check

    Returns:
        Boolean indicating if the text is a URL
    """
    url_pattern = re.compile(
        r"^https?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain
        r"localhost|"  # localhost
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # or ipv4
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return bool(url_pattern.match(text))


def download_image(url):
    """
    Download an image from a URL using standard library

    Args:
        url: URL to download from

    Returns:
        Path to the downloaded image
    """
    try:
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        temp_path = pathlib.Path(temp_file.name)

        # Set up request with a user agent to avoid 403 errors
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        req = urllib.request.Request(url, headers=headers)

        # Download the image
        with urllib.request.urlopen(req) as response, temp_file:
            temp_file.write(response.read())

        return str(temp_path)
    except urllib.error.URLError as e:
        print(f"Error downloading image: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def parse_arguments():
    """
    Parse command line arguments

    Returns:
        Parsed command line arguments
    """
    parser = argparse.ArgumentParser(description="Extract text from images using OCR")
    parser.add_argument("image_path", help="Path to the image file or URL to an image")
    parser.add_argument("--output", "-o", help="Output file path (optional)")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Print additional information"
    )

    return parser.parse_args()


def save_text_to_file(text, file_path, verbose=False):
    """
    Save text to a file

    Args:
        text: Text to save
        file_path: Path to the output file
        verbose: Whether to print additional information
    """
    output_path = pathlib.Path(file_path)
    with output_path.open("w", encoding="utf-8") as f:
        f.write(text)

    if verbose:
        print(f"Text saved to: {output_path}")


def main():
    """
    Main entry point for the CLI application

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    args = parse_arguments()

    try:
        image_path = args.image_path

        # Handle URL input
        if is_url(image_path):
            if args.verbose:
                print(f"Downloading image from URL: {image_path}")
            image_path = download_image(image_path)
            if args.verbose:
                print(f"Downloaded to: {image_path}")

        if args.verbose:
            print(f"Processing image: {image_path}")

        # Always use the fallback module for now
        from .fallback import extract_text

        # Debug what's happening
        if args.verbose:
            print("Using fallback OCR module", file=sys.stderr)

        extracted_text = extract_text(image_path)

        # Cleanup temp file if it was a URL
        if is_url(args.image_path) and pathlib.Path(image_path).exists():
            try:
                pathlib.Path(image_path).unlink()
                if args.verbose:
                    print(f"Removed temporary file: {image_path}")
            except Exception as e:
                if args.verbose:
                    print(
                        f"Warning: Failed to remove temporary file: {e}",
                        file=sys.stderr,
                    )

        # Output the text
        if args.output:
            save_text_to_file(extracted_text, args.output, args.verbose)
        else:
            print(extracted_text)

        return 0

    except Exception as e:
        print(f"Error during processing: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
