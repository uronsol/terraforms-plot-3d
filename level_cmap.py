import sys

import numpy as np
import pandas as pd
from PIL import Image

import plot_terrain


def main():
    if len(sys.argv) != 3:
        sys.exit(f'Usage: {sys.argv[0]} <level> <output_path>')

    level = int(sys.argv[1])

    df = pd.read_csv('terraforms.csv', index_col=0)
    df = df[df.Level == level]
    coord_map = {(row['X Coordinate'], row['Y Coordinate']): i
                 for i, row in df.iterrows()}

    output = terrain_image(coord_map)
    img = Image.fromarray(output)
    img.save(sys.argv[2], format='png')


def terrain_image(coord_map, interpolation=1):
    factor = 32 * interpolation
    width = max(x for x, _ in coord_map.keys()) + 1
    height = max(y for _, y in coord_map.keys()) + 1
    output = np.zeros((width * factor, height * factor, 4), dtype=np.uint8)
    for (x_coord, y_coord), token_id in coord_map.items():
        off_x = x_coord * factor
        off_y = y_coord * factor
        _, _, z, cmap = plot_terrain.terrain(token_id, interpolation)
        z = (z - z.min()) / (z.max() - z.min())  # Normalize to [0,1]
        output[off_y:off_y + factor, off_x:off_x + factor] = cmap(z.T) * 255
    return output


if __name__ == '__main__':
    sys.exit(main())
