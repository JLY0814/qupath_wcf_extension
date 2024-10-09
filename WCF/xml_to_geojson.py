import xml.etree.ElementTree as ET
import json
import math
import openslide
import os
import numpy as np
import argparse


# def bbox_to_circle_points(top_right, bottom_left, num_points=100):
#     x1, y1 = top_right
#     x2, y2 = bottom_left
#     center_x = (x1 + x2) / 2
#     center_y = (y1 + y2) / 2
#     radius = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / 2
#
#     angle_step = 2 * math.pi / num_points
#     circle_points = [
#         [center_x + radius * math.cos(i * angle_step), center_y + radius * math.sin(i * angle_step)]
#         for i in range(num_points)
#     ]
#     circle_points.append(circle_points[0])
#     return circle_points

def bbox_to_circle_points(top_right, bottom_left, num_points=100):
    x1, y1 = top_right
    x2, y2 = bottom_left
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    radius_x = abs(x1-x2) / 2
    radius_y = abs(y1-y2) / 2
    radius = min(radius_x, radius_y)


    angle_step = 2 * math.pi / num_points
    circle_points = [
        [center_x + radius * math.cos(i * angle_step), center_y + radius * math.sin(i * angle_step)]
        for i in range(num_points)
    ]
    circle_points.append(circle_points[0])
    return circle_points



# def int_to_rgb_array(color_int):
#     red = (color_int >> 16) & 255
#     green = (color_int >> 8) & 255
#     blue = color_int & 255
#     return [red, green, blue]

def int_to_rgb_array(color_int):
    color_mapping = {
        255: ([255, 0, 0], "1"),
        16711680: ([0, 0, 139],"2"),  # Dark Blue
        16776960: ([173, 216, 230],"3" ), # Light Blue
        65280: ([144, 238, 144],"4"), # Light Green
        32768: ([0, 100, 0], "5")# Dark Green

        # 16711680: 139 ,  # Dark Blue
        # 16776960: 59,  # Light Blue
        # 65280: 220,  # Light Green
        # 32768: 109 # Dark Green
    }
    return color_mapping.get(color_int, ([255,255,0],"correct"))  # Default to black if color is not in the mapping


def rotate_point_90_ccw(x, y, image_height, file_type):
    if file_type == '.svs':
        return x, y
    elif file_type == '.scn':
        return y, image_height - x
    else:
        raise ValueError("Unsupported file type")
def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    annotations = []

    for annotation in root.findall('.//Annotation'):
        line_color = int(annotation.get('LineColor'))
        for region in annotation.findall('.//Region'):
            vertices = region.find('Vertices')
            if vertices is not None:
                vertex_list = [(float(vertex.get('X')), float(vertex.get('Y'))) for vertex in
                               vertices.findall('Vertex')]
                if len(vertex_list) == 2:
                    annotations.append({
                        'top_right': vertex_list[0],
                        'bottom_left': vertex_list[1],
                        'line_color': line_color
                    })
    return annotations



def create_geojson(annotations, image_height, file_type):
    features = []
    for annotation in annotations:
        top_right = (annotation['top_right'][0], annotation['top_right'][1])
        bottom_left = (annotation['bottom_left'][0], annotation['bottom_left'][1])

        circle_points = bbox_to_circle_points(top_right, bottom_left)
        rotated_circle_points = [rotate_point_90_ccw(x, y, image_height, file_type) for x, y in circle_points]

        color_int = annotation['line_color']
        color_array, name = int_to_rgb_array(color_int)

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [rotated_circle_points]
            },
            "properties": {
                "classification": {
                    "name": name,
                    "color": color_array
                }
            }
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    return geojson

def save_geojson(geojson, output_file):
    with open(output_file, 'w') as f:
        json.dump(geojson, f, indent=2)


def process_files(scn_dir, xml_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(scn_dir):
        if file.endswith('.scn') or file.endswith('.svs'):
            file_path = os.path.join(scn_dir, file)
            file_type = os.path.splitext(file)[1]  # Get the file extension

            # Get the base name without the extension
            base_name = file[:-len(file_type)]  # Remove file extension

            # Check for XML files in the xml_dir that contain the base name
            xml_files = [f for f in os.listdir(xml_dir) if f.endswith('.xml') and base_name in f]
            if xml_files:
                for xml_file in xml_files:
                    xml_path = os.path.join(xml_dir, xml_file)
                    slide = openslide.OpenSlide(file_path)
                    try:
                        image_width = int(slide.properties['openslide.bounds-width'])
                        image_height = int(slide.properties['openslide.bounds-height'])
                    except:
                        image_width, image_height = slide.level_dimensions[0]

                    annotations = parse_xml(xml_path)
                    geojson = create_geojson(annotations, image_height, file_type)  # Pass the file type

                    output_file = os.path.join(output_dir, xml_file.replace('.xml', '.geojson'))
                    save_geojson(geojson, output_file)
                    print(f"Processed {file} and saved GeoJSON to {output_file}")
            else:
                print(f"XML file for {file} not found")

# Replace these paths with your actual directories
# scn_dir = '/data/CircleNet/data/new_data_for_miccai_paper/test/test_geojson'
# xml_dir = '/data/CircleNet/data/new_data_for_miccai_paper/test/test_geojson'
# output_dir = '/data/CircleNet/data/new_data_for_miccai_paper/test/test_geojson/test_result_geojson'


parser = argparse.ArgumentParser(description="Second script processing")
parser.add_argument("--wsi_dir", required=True, help="Directory for demo")
parser.add_argument("--xml_dir", required=True, help="Ground truth directory")
args = parser.parse_args()

# Generate output_dir by appending "_geojson" to the last part of xml_dir
xml_base_name = os.path.basename(args.xml_dir)  # Get the last folder name
output_dir = os.path.join(os.path.dirname(args.xml_dir), f"{xml_base_name}_geojson")  # Create new directory path

os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist

# Output the generated output_dir for verification
print(f"Output directory: {output_dir}")



process_files(args.wsi_dir, args.xml_dir, output_dir)

