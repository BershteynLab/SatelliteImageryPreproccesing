import matplotlib.pyplot as plt
import mmcv
import pandas as pd
import os
import sys
from utils import process_file

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
                img = mmcv.imread(os.path.join(input_folder, image_name))

                # Load labels data (assuming img_labels is a DataFrame with x1, y1, x2, y2, ..., xn, yn columns)
                # Replace this line with the actual loading of your labels data
                        # Loop through each file in input folder

                image_label_path = os.path.join(input_folder, image_name.replace('.png', '.txt'))
                
                process_file(image_label_path, input_folder)
                print(f"Processed {image_label_path}")
                img_labels = pd.read_csv(image_label_path,
                            sep=' ',
                            names=['x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4', 'label', 'difficulty'])

                # Create subplots
                fig, axes = plt.subplots(1, 2, figsize=(20, 10))

                # Plot image without labels on the first subplot
                axes[0].imshow(mmcv.bgr2rgb(img))
                axes[0].set_title('Image without Labels')

                # Plot image with labels on the second subplot
                axes[1].imshow(mmcv.bgr2rgb(img))
                for index, row in img_labels.iterrows():
                    x = row[['x1', 'x2', 'x3', 'x4', 'x1']]
                    y = row[['y1', 'y2', 'y3', 'y4', 'y1']]
                    axes[1].plot(x, y, '-', color='red')
                    axes[1].plot(x, y, 'o', color='red')
                axes[1].set_title('Image with Labels')
                print("Created image with labels: ", image_name)

                plt.suptitle(image_name, fontsize=16)
                output_file_path = os.path.join(output_folder, image_name)
                print(f"Saving comparison image to {output_file_path}")
                plt.savefig(output_file_path)
            else:
                continue

    except FileNotFoundError:
        print(f"Folder not found: {input_folder}")
        sys.exit(1)

if __name__ == "__main__":
    main()