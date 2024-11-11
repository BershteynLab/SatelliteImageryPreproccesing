
import pandas as pd
from pathlib import Path
import os
import shutil

def main():
    # Existing older with drone data, split into images, train, and val folders
    DRONE_DATA_FOLDER = Path("drone_data_w_blanks")
    DRONE_TRAIN = DRONE_DATA_FOLDER / "train"
    DRONE_VAL = DRONE_DATA_FOLDER / "val"

    # Specify folders within input folder
    IMAGE_FOLDER = DRONE_DATA_FOLDER / "images"

    # Desired output folder name/location
    OUTPUT_FOLDER = Path("drone_data_crossvalidation")

    # Create output folder and subfolders
    image_output_folder = OUTPUT_FOLDER/ "images"
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(image_output_folder, exist_ok=True)
    print(f"Output folder created: {OUTPUT_FOLDER}")

    # Prefixes of cemetary and non-cemetary file names
    cemetaries = ["DAR_UNLABLED_1", "DAR_UNLABLED_2", "DAR_UNLABLED_3", "DAR_UNLABLED_4", "DAR_UNLABLED_5", "DAR_UNLABLED_6", "DAR_UNLABLED_7",
                "Ismail Cementary", "Ismaili Cemetery", "Karume Cemetery", "Mburahati", "Mianzini Graveyard", "Ubungo", "Msasani", "Mikocheni"]
    noncemetaries = ["DAR_FIELDS_AND_BUILDINGS_2", "DAR_FIELDS_AND_BUILDINGS", "DAR_NONBURIAL_BUILDINGS", "DAR_NONBURIAL_EMPTYFIELDCARDS"]

    def copy_files(input_folder, output_folder):
        """Copies all files from input_folder to output_folder"""
        for filename in os.listdir(input_folder):
            file_path = os.path.join(input_folder, filename)
            image_path = os.path.join(output_folder, filename)
            shutil.copy2(file_path, image_path)
            #print(f"Copied {filename} to {image_path}")

    # Copy all images to an image file inside the output folder
    copy_files(IMAGE_FOLDER, image_output_folder)

    # Create one folder of all text labels in the output folder
    ALL_LABELS_PATH = f"{OUTPUT_FOLDER}/all_labels"
    os.makedirs(ALL_LABELS_PATH, exist_ok=True)

    copy_files(DRONE_TRAIN, ALL_LABELS_PATH)
    copy_files(DRONE_VAL, ALL_LABELS_PATH)

    # Create train and test folders for each cemetary
    for cemetary in cemetaries:
        os.makedirs(f"{OUTPUT_FOLDER}/{cemetary}_train", exist_ok=True)
        os.makedirs(f"{OUTPUT_FOLDER}/{cemetary}_test", exist_ok=True)
        print(f"Created train and test folders for {cemetary}")

    for file in os.listdir(ALL_LABELS_PATH):
        file_path = os.path.join(ALL_LABELS_PATH, file)  

        # Check if file is a cemetary file
        matching_cemetaries = [cemetary for cemetary in cemetaries if file.startswith(cemetary)]

        # If file is a cemetary file
        if len(matching_cemetaries) > 0:     

            # Get matching cemetary
            cemetary = matching_cemetaries[0]    

            test_folder = f"{OUTPUT_FOLDER}/{cemetary}_test"

            # Copy to the test folder of the matching cemetery
            test_path = os.path.join(test_folder, file)
            try:
                shutil.copy(file_path, test_path)
            except FileNotFoundError:
                print(f"File {file} not copied to {test_folder}")

            # Create list of all cemetaries except the matching one
            train_cemetaries = cemetaries.copy()
            train_cemetaries.remove(cemetary)
            print("train_cemetaries", train_cemetaries)
            
            # Copy to train folder of all other cemetaries
            for train in train_cemetaries:
                print(train)
                train_folder = f"{OUTPUT_FOLDER}/{train}_train"
                train_path = os.path.join(train_folder, file)
                try:
                    shutil.copy(file_path, train_path)
                except FileNotFoundError:
                    print(f"File {file} not copied to {train_folder}")
        else:
            # Copy non-cemetary files to train folders for all cemetaries
            for cemetary in cemetaries:
                train_folder = f"{OUTPUT_FOLDER}/{cemetary}_train"
                train_path = os.path.join(train_folder, file)
                try:
                    shutil.copy(file_path, train_path)
                except FileNotFoundError:
                    print(f"File {file} not copied to {train_folder}")


if __name__ == "__main__":
    main()



