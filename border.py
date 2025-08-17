import cv2
import os
import glob
import argparse


def add_border(image_path):
    """Adds a 5% replicated border to an image"""
    try:
        # Read the image
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            print(f"Error: Could not read image {image_path}")
            return

        h, w = img.shape[:2]

        # Calculate the padding (5% of the smallest dimension)
        pad = int(0.05 * min(h, w))

        # Apply padding by replicating the borders
        out = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_REPLICATE)

        # Save the image, overwriting the original
        cv2.imwrite(image_path, out)
        print(f"Processed and saved image: {image_path}")

    except Exception as e:
        print(f"An error occurred while processing {image_path}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Enlarge image(s) by adding a 5% replicated border."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-i", "--image", help="Path to a specific image to process.")
    group.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Process all .png images in the 'media' directory.",
    )

    args = parser.parse_args()

    if args.image:
        if os.path.isfile(args.image):
            add_border(args.image)
        else:
            print(f"Error: File not found at '{args.image}'")
    elif args.all:
        media_dir = "media"
        if not os.path.isdir(media_dir):
            print(f"The directory '{media_dir}' does not exist.")
            return

        image_paths = glob.glob(os.path.join(media_dir, "*.png"))
        if not image_paths:
            print(f"No .png images found in the '{media_dir}' directory.")
            return

        print(f"{len(image_paths)} images found. Starting processing...")
        for path in image_paths:
            add_border(path)
        print("All images have been processed.")


if __name__ == "__main__":
    main()
