"""
Collection of graph layout algorithms.
"""

import numpy as np
from networkx.drawing.layout import rescale_layout, _process_params

def shell_layout(G, nlist=None, center=None, nsize=10):

    G, center = _process_params(G, center, 2)

    radius = 0
    L = 10 * nsize

    npos = {}
    for nodes in nlist:
        step = (2 * np.pi) / len(nodes)
        theta = np.linspace(0, 1, len(nodes) + 1)[:-1] * 2 * np.pi
        theta = theta.astype(np.float32)
        radius = max(L / step, radius * 2)
        pos = np.column_stack([np.cos(theta), np.sin(theta)])
        pos = rescale_layout(pos, scale=radius / len(nlist)) + center
        assert len(pos) == len(nodes), f"{len(pos)} != {len(nodes)}"
        npos.update(zip(nodes, pos))

    return npos