import sys
import os

from utils import process_file

def main():

    if len(sys.argv) !=2:
        print("Usage: python create_mmrotate_folder.py <input_folder>")
        sys.exit(1)
    
    input_folder = sys.argv[1]
    folder_name = "satellite_mmrotate"

    try:

        # Create file structure
        parent_folder = os.path.dirname(input_folder)
        output_folder = f"{parent_folder}/{folder_name}"
        train_folder = f"{output_folder}/train"
        val_folder = f"{output_folder}/val"
        image_folder = f"{output_folder}/images"
        os.makedirs(output_folder, exist_ok=True)
        os.makedirs(train_folder, exist_ok=True)
        os.makedirs(val_folder, exist_ok=True)
        os.makedirs(image_folder, exist_ok=True)
        print(f"Ouptut folder created: {output_folder}")

        # Loop through each file in input folder
        for filename in os.listdir(input_folder):
            # Move images to image folder
            if filename.endswith(".png"):
                file_path = os.path.join(input_folder, filename)
                image_path = os.path.join(image_folder, filename)
                os.rename(file_path, image_path)
                print(f"Moved {filename} to {image_path}")

            # Process .txt files and move to train/val folders
            elif filename.endswith(".txt"):
                file_path = os.path.join(input_folder, filename)

                train = ["DAR_UNLABLED", "Ismail Cementery", "Ismaili Cemetery", "Ubongo", "Msasani"]

                # if filename includes any of the train cemetaries, move to train folder
                if any(cemetary in filename for cemetary in train):
                    process_file(file_path, train_folder)
                    print("File written")
                else:
                    process_file(file_path, val_folder)

    except FileNotFoundError:
        print(f"File not found: {input_folder}")
        sys.exit(1)

if __name__ == "__main__":
    main()