import matplotlib.pyplot as plt
import mmcv
import pandas as pd
import os
import sys

import cv2
import numpy as np

def is_shape_primarily_white(image_path, coordinates):
    image = cv2.imread(image_path)

    # Check if the image is successfully loaded
    if image is None:
        print("Error: Unable to load the image.")
        return None  # or return an appropriate value

    # Convert the coordinates to a numpy array
    points = np.array(coordinates, np.int32).reshape((-1, 2))

    # Create a mask for the specified shape
    mask = np.zeros_like(image[:, :, 0])
    cv2.fillPoly(mask, [points], 255)

    # Convert the masked region to HSV color space
    hsv_roi = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    roi = cv2.bitwise_and(hsv_roi, hsv_roi, mask=mask)

    # Define a lower and upper range for white color in HSV
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])

    # Create a mask for the white color
    white_mask = cv2.inRange(roi, lower_white, upper_white)

    # Calculate the percentage of white pixels
    white_pixel_count = np.sum(white_mask == 255)
    total_pixel_count = np.sum(mask == 255)

    # Check if the denominator is zero
    if total_pixel_count == 0:
        print("Error: Divide by zero. The mask has no white pixels.")
        return None  # or return an appropriate value

    # Calculate the percentage of white pixels
    white_percentage = white_pixel_count / total_pixel_count

    # Return the percentage of white pixels
    return white_percentage

def format_line(line):
    # Remove index and commas, and line break from row
    formatted_row = ' '.join(line.strip().split(',')[1:])

    # Add class label and perplexity to each row
    formatted_row += " grave 0\n"

    return formatted_row


def process_file(input_file_path, output_folder):
    try:
        with open(input_file_path, 'r') as infile:
            content = infile.readlines()

        # Format each line and write to modified output file
        output_file_path = os.path.join(output_folder, f"{os.path.basename(input_file_path)}")
        with open(output_file_path, 'w') as outfile:
            for line in content:
                modified_line = format_line(line)
                outfile.write(modified_line)

    except FileNotFoundError:
        print(f"File not found: {input_file_path}")

def main():

    if len(sys.argv) !=3:
        print("Usage: python create_mmrotate_folder.py <input_folder> <output_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_name = sys.argv[2]
    output_folder = os.path.join(os.path.basename(input_folder), output_name)
    os.makedirs(output_folder, exist_ok=True)

    try:
        # Loop through files in folder
        for image_name in os.listdir(input_folder):
            if image_name.endswith(".png"):
                print(f"Processing {image_name}")
                # Load the image
                image_path = os.path.join(input_folder, image_name)
                img = cv2.imread(os.path.join(image_path))

                # Load labels data (assuming img_labels is a DataFrame with x1, y1, x2, y2, ..., xn, yn columns)
                # Replace this line with the actual loading of your labels data
                        # Loop through each file in input folder

                image_label_path = os.path.join(input_folder, image_name.replace('.png', '.txt'))
                
                print(f"Processed {image_label_path}")
                df = pd.read_csv(image_label_path,
                            sep=',',
                            names=['index', 'x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4'],
                            index_col=0)

                index_list = []

                for index, row in df.iterrows():
                    
                    coordinates = [row['x1'], row['y1'], row['x2'], row['y2'], row['x3'], row['y3'], row['x4'], row['y4']]
                    result = is_shape_primarily_white(image_path, coordinates)
                    if result > 0:
                        index_list.append(index)
                    else:
                        continue

                subset_df = df.loc[index_list]

                subset_df['label'] = 'grave'
                subset_df['difficulty'] = 0
                print(subset_df.head())

                output_file_path = os.path.join(output_folder, image_name.replace('.png', '.txt'))
                print(f"Saving labels to {output_file_path}")
                print(subset_df.head())
                subset_df.to_csv(output_file_path, header=False, index=True, sep=" ")
                #Save image to ouptut folder
                output_image_path = os.path.join(output_folder, image_name)
                print(f"Saving image to {output_image_path}")
                cv2.imwrite(output_image_path, img)
            else:
                continue

    except FileNotFoundError:
        print(f"Folder not found: {input_folder}")
        sys.exit(1)

if __name__ == "__main__":
    main()