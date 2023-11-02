import copy
from math import asin, cos, pi, sin, sqrt
import re
import labelbox
import os
import argparse
from typing import Dict, List
from itertools import chain, combinations
from pathlib import Path
import os


LB_API_KEY = os.environ["LABELBOXAPI"]
drone_project_id = "clmewgs9a0wtp070o67vm1v9r"
DEFAULT_PROJECT_ID = drone_project_id

def get_client():
    return labelbox.Client(api_key = LB_API_KEY)


def grab_results(project_id):
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
    return labels.result

def get_simplication_loss(points : List[Dict[str,float]]):
    triangle_area = 0.5 * (points[0]['x'] * (points[1]["y"] - points[2]["y"]) + points[1]["x"] * (points[2]['y'] - points[0]['y']) + points[2]["x"]
                  * (points[0]["y"] - points[1]["y"]))
    return triangle_area

def remove_excess_points(points : List[Dict[str,float]]):
    index_and_cost = []
    i = 1
    for left, middle, right in zip(points[:-2], points[1:-1], points[2:]):
        index_and_cost += [(i, get_simplication_loss([left, middle, right]))]
        i += 1
    
    index_and_cost_2_keep = sorted(index_and_cost, key= lambda x: -x[-1])[:3]
    index_2_keep, _ = zip(*index_and_cost_2_keep)
    return [point for i, point in enumerate(points) if i in ((0,) + index_2_keep)]

def add_extra_point(points : List[Dict[str, float]]):
    edges = combinations(points,2)
    hypotenuse = sorted(edges, key=lambda p1p2: (p1p2[0]['x'] - p1p2[1]['x'])**2 + (p1p2[0]['y'] - p1p2[1]['y'])**2)[-1]
    b = [point for point in points if not (point in hypotenuse) ][0]
    bisect_point = {"x":(hypotenuse[0]['x'] + hypotenuse[1]['x'])/2, "y": (hypotenuse[0]['y'] + hypotenuse[1]['y'])/2}
    bisect_distance = sqrt((b['x'] - bisect_point['x'])**2 + (b['y'] - bisect_point['y'])**2)
    bisect_angle = asin((bisect_point['y'] - b['y'] )/ bisect_distance)
    bisect_angle = bisect_angle if b['x'] < bisect_point["x"] else pi - bisect_angle
    diagonal_dist = bisect_distance * 2
    diagonal_y = round(sin(bisect_angle) * diagonal_dist,1)
    diagonal_x = round(cos(bisect_angle) * diagonal_dist,1)
    new_point = {"x" : max(b['x'] + diagonal_x,0), "y" : max(b['y'] + diagonal_y,0)} 
    if (points[0] == b):
        return points[:2] + [new_point] + points[2:]
    elif (points[1] == b):
        return points[:3] + [new_point] + points[3:]
    elif (points[2] == b):
        return points[:1] + [new_point] + points[1:]
    else:
        raise Exception("Three points in rectangle and somehow I couldnt figure it out")

def process_polygon(lb_polygon : List[Dict[str, float]]) -> str: 
    formatted_points = list(
                            chain(
                                    *[(
                                        str(round(point["x"],1)), 
                                        str(round(point["y"],1))
                                       ) for point in lb_polygon]
                                )
                            )
    return " ".join(formatted_points) + " grave 0"        

def results_to_DOTA(results):
    result_strings = {}
    for result in results:
        objects = list(result["projects"].values())[0]["labels"][0]["annotations"]["objects"]
        poly_strings = []
        for object in objects:
            points = object['polygon']
            if len(points) > 5:
                points = remove_excess_points(points)
            elif len(points) == 5:
                points = points[:-1]
            else:
                points = add_extra_point(points)[:-1]
            poly_strings += [process_polygon(points)]
        result_strings[result["data_row"]["external_id"]] = poly_strings
    return result_strings

def tiled_results_to_fullimage(results):
    results = copy.deepcopy(results)
    for i_result in range(len(results)):
        filename = results[i_result]["data_row"]["external_id"]
        digit_text = re.compile(r"(_\d_\d)").search( filename ).group().split("_")
        i_row = int(digit_text[1])
        i_col = int(digit_text[2])

        for project in results[i_result]["projects"]:
            for i_label in range(len(results[i_result]["projects"][project]["labels"])):
                for i_object in range(len(results[i_result]["projects"][project]["labels"][i_label]["annotations"]["objects"])):
                    for i_point in range(len(results[i_result]["projects"][project]["labels"][i_label]["annotations"]["objects"][i_object]['polygon'])):
                        results[i_result]["projects"][project]["labels"][i_label]["annotations"]["objects"][i_object]['polygon'][i_point]["x"] += i_col*1000
                        results[i_result]["projects"][project]["labels"][i_label]["annotations"]["objects"][i_object]['polygon'][i_point]["y"] += i_row*1000
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='Download Labels',
                        description='Download labelbox annotations to DOTA')
    parser.add_argument('-p', '--project_id', default=DEFAULT_PROJECT_ID, help=f"Labelbox project ID. \n for example, use {drone_project_id} for drone labels")
    parser.add_argument('-o', '--output_folder', default="./")
    parser.add_argument('--fullimage_labels', action=argparse.BooleanOptionalAction) 
    args = parser.parse_args()
    results = grab_results(args.project_id)
    if args.fullimage_labels:
        results = tiled_results_to_fullimage(results)
    dota_outputs = results_to_DOTA(results)
    output_folder = Path(args.output_folder)
    if not output_folder.exists():
        os.mkdir(output_folder)
    for dota_key in dota_outputs.keys():
        output_path = Path(args.output_folder) / Path(dota_key.replace(".png",".txt"))
        with open(output_path, "w+") as f:
            f.write("\n".join(dota_outputs[dota_key]))
