import os
import sys

from utils import process_file

# Script to modify the Satelitte imagery label folder with comma seperated .txtfiles to a format compatible with MMRotate

def main():

    # Check for file path argument
    if len(sys.argv) != 3:
        print("Usage: python modify_satellite_labels.py <file_path> <output_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    try:
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Loop through each file in input folder
        for filename in os.listdir(input_folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(input_folder, filename)
                process_file(file_path, output_folder)

    except FileNotFoundError:
        print(f"File not found: {input_folder}")
        sys.exit(1)

if __name__ == "__main__":
    main()