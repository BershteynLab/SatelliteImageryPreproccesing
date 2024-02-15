import os

def format_line(line):
    # Remove index and commas, and line break from row
    formatted_row = ' '.join(line.strip().split(',')[1:])

    # Add class label and perplexity to each row
    formatted_row += " grave 0"
    
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