import os
import urllib
import argparse
from pathlib import Path
from download_labels import grab_results, DEFAULT_PROJECT_ID, drone_project_id

def download_image(result_set, folder):
    url = result_set["data_row"]["row_data"]
    filename = result_set["data_row"]["external_id"]
    urllib.request.urlretrieve(url, folder / filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='Download images',
                        description='Download labelbox images')
    parser.add_argument('-p', '--project_id', default=DEFAULT_PROJECT_ID, help=f"Labelbox project ID. \n for example, use {drone_project_id} for drone images")
    parser.add_argument('-o', '--output_folder', default="./")
    args = parser.parse_args()
    results = grab_results(args.project_id)
    output_path = Path(args.output_folder)
    if not output_path.exists():
        os.mkdir(output_path)
    for result_set in results:
        download_image(result_set, output_path)

    