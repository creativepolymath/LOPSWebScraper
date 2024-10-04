import pandas as pd
from PIL import Image
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
    for color in colors:
        img = Image.new('RGB', (100, 100), f"#{color['rgb_hex']}")
        img.save(f"{color['name']}.png")

    return df

if __name__ == "__main__":
    df = extract_colors_from_xml('palette.xml')
    print(df)
