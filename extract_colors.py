import pandas as pd
import xml.etree.ElementTree as ET


def extract_colors_from_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    colors = []
    for color in root.findall('color'):
        name = color.get('name')
        rgb_hex = color.get('rgb')
        colors.append({'name': name, 'rgb_hex': rgb_hex})

    df = pd.DataFrame(colors)
    return df

if __name__ == "__main__":
    df = extract_colors_from_xml('palette.xml')
    print(df)
