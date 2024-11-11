from pathlib import Path
import os

BLANK_DATA_FOLDER = Path("drone_no_graves_images_tiled")
OUTPUT_FOLDER = Path("drone_data_w_blanks")
IMAGE_FOLDER = OUTPUT_FOLDER / "images"
LABEL_FOLDER = OUTPUT_FOLDER / "train"

def main():

    # Create file structure
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(IMAGE_FOLDER, exist_ok=True)
    os.makedirs(LABEL_FOLDER, exist_ok=True)
    print(f"Output folder created: {OUTPUT_FOLDER}")

    # Loop through each file in input folder
    for filename in os.listdir(BLANK_DATA_FOLDER):
        # Move images to image folder
        if filename.endswith(".png"):
            file_path = BLANK_DATA_FOLDER / filename
            image_path = IMAGE_FOLDER / filename
            os.rename(file_path, image_path)
            print(f"Moved {filename} to {image_path}")


            # Create blank label file
            txt_filename = filename.replace(".png", ".txt")
            print(txt_filename)

            with open(LABEL_FOLDER / txt_filename, "w") as f:
                f.write("")

            print(f"Created blank label file for {filename}")

if __name__ == "__main__":
    main()