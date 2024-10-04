import pandas as pd
import webcolors
import xml.etree.ElementTree as ET

def closest_color(requested_color):
    min_colors = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors)]

def get_color_name(rgb_hex):
    try:
        return webcolors.hex_to_name(f"#{rgb_hex}")
    except ValueError:
        rgb = tuple(int(rgb_hex[i:i+2], 16) for i in (0, 2, 4))
        return closest_color(rgb)

def extract_colors_from_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    colors = []
    for color in root.findall('color'):
        name = color.get('name')
        rgb_hex = color.get('rgb')
        color_name = get_color_name(rgb_hex)
        colors.append({'name': name, 'rgb_hex': rgb_hex, 'color_name': color_name})

    df = pd.DataFrame(colors)
    return df

if __name__ == "__main__":
    df = extract_colors_from_xml('palette.xml')
    print(df)
