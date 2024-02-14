import os
import sys

# Script to modify the Satelitte imagery label folder "overlayed_boxes" to a format compatible with MMRotate

def format_line(line):
    # Remove index and commas from row
    formatted_row = ' '.join(line.split(',')[1:])

    # Add class label and perplexity to each row
    formatted_row += " grave 0\n"

    return formatted_row

def process_file(input_file_path, output_folder):
    try:
        with open(input_file_path, 'r') as infile:
            content = infile.readlines()

        # Format each line and write to modified output file
        output_file_path = os.path.join(output_folder, f"modified_{os.path.basename(input_file_path)}")
        with open(output_file_path, 'w') as outfile:
            for line in content:
                modified_line = format_line(line)
                outfile.write(modified_line)

    except FileNotFoundError:
        print(f"File not found: {input_file_path}")

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