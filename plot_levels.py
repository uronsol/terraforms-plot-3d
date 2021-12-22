import sys

import matplotlib.pyplot as plt
import pandas as pd

import plot_terrain


def main():
    if len(sys.argv) != 3:
        sys.exit(f'Usage: {sys.argv[0]} <min_level> <max_level>')

    min_level = int(sys.argv[1])
    max_level = int(sys.argv[2])

    df = pd.read_csv('terraforms.csv', index_col=0)
    df = df[(df.Level >= min_level) & (df.Level <= max_level)]
    coord_map = {}
    for i, row in df.iterrows():
        x, y, z = row['X Coordinate'], row['Y Coordinate'], row['Level'] - 1
        coord_map[x, y, z] = i
    plot_terrains(coord_map, interpolation=0.5)


def plot_terrains(mapping, interpolation=1):
    ax = plt.axes(projection='3d')
    for (coord_x, coord_y, coord_z), token_id in mapping.items():
        x, y, z, cmap = plot_terrain.terrain(token_id, interpolation)
        x += coord_x
        y += coord_y
        z += coord_z * 90000  # 90000 is arbitrary
        ax.plot_surface(x, y, z, cmap=cmap)
        ax.set_zticklabels([])
    plt.show()


if __name__ == '__main__':
    sys.exit(main())
