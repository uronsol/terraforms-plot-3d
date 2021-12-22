import json
import pickle
import sys
from pathlib import Path

import numpy as np
import scipy.interpolate
from web3 import Web3

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


RPC_URL = 'https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161'
CONTRACT_ADDR = '0x4E1f41613c9084FdB9E34E11fAE9412427480e56'

TOPOGRAPHY = [
    -26000,
    -22000,
    -20000,
    -12000,
    -4000,
    4000,
    12000,
    18000,
]


def main():
    if len(sys.argv) != 2:
        sys.exit(f'Usage: {sys.argv[0]} <token_id>')

    token_id = int(sys.argv[1])
    plot_terrain(token_id, interpolation=16)


def plot_terrain(token_id, interpolation=1):
    ax = plt.axes(projection='3d')
    x, y, z, cmap = terrain(token_id, interpolation)
    ax.plot_surface(x, y, z, cmap=cmap)
    ax.set_zticklabels([])
    plt.show()


def terrain(token_id, interpolation=1):
    # Get terrain values and colors
    path = Path(f'metadata/{token_id}.pkl')
    if path.exists():
        with open(path, 'rb') as f:
            z, colors = pickle.load(f)
    else:
        z, colors = retrieve_metadata(token_id)
        with open(path, 'wb') as f:
            pickle.dump((z, colors), f)

    # Get x, y, z values
    z = np.array(z).T
    x = np.linspace(0, 1, 32)
    y = np.linspace(0, 1, 32)
    if interpolation != 1:
        f = scipy.interpolate.interp2d(x, y, z, kind='cubic')
        x = np.linspace(0, 1, int(32 * interpolation))
        y = np.linspace(0, 1, int(32 * interpolation))
        z = f(x, y)
    x, y = np.meshgrid(x, y)

    # Determine the appropriate colormap
    colors = colors[8::-1] + [colors[0]]
    nodes = (np.array(TOPOGRAPHY, dtype=float) - z.min()) / (z.max() - z.min())
    nodes = [0.] + list(nodes.clip(0, 1)) + [1.]
    cmap = LinearSegmentedColormap.from_list('test', list(zip(nodes, colors)))

    return x, y, z, cmap


def retrieve_metadata(token_id):
    with open('contract_abi.json', 'r') as f:
        contract_abi = json.load(f)
    web3 = Web3(Web3.HTTPProvider(RPC_URL))
    contract = web3.eth.contract(CONTRACT_ADDR, abi=contract_abi)

    # Return the terrain values and the color scheme
    z = contract.functions.tokenTerrainValues(token_id).call()
    supplemental = contract.functions.tokenSupplementalData(token_id).call()
    return z, supplemental[9]


if __name__ == '__main__':
    sys.exit(main())
