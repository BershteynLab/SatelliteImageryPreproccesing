import json
import labelbox
import os
import argparse

LB_API_KEY = os.environ["LABELBOXAPI"]
DEFAULT_PROJECT_ID = 'cllnzoauf18sv07xrh3mx3zr5'
def get_client():
    return labelbox.Client(api_key = LB_API_KEY)

def download_results(project_id, out_file):
    client = get_client()
    project = client.get_project(project_id)

    labels = project.export_v2(params={
        "data_row_details": True,
        "metadata_fields": True,
        "attachments": True,
        "project_details": True,
        "performance_details": True,
        "label_details": True,
        "interpolated_frames": True
    })
    labels.wait_till_done()
    results = labels.result
    with open(out_file, "w+") as f:
        f.write(json.dumps(results))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='Download Labels',
                        description='Download labelbox annotations to json')
    parser.add_argument('-f', '--filename', default="labelbox.json")
    parser.add_argument('-p', '--project_id', default=DEFAULT_PROJECT_ID)
    args = parser.parse_args()
    download_results(args.project_id, args.filename)