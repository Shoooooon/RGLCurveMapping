

## this is a python executable that will be called from GH to get curve data using Connecting_Points.py


import Connecting_Points as cp

from sys import argv

script, curve = argv

curve = [int(c) for c in curve]

triangulation = [(~1, ~8, ~0), (~7, 3, 8), (~2, ~6, 7), (~5, 2, 6), (~3, ~4, 5), (0, 1, 4)]
edges = [1, 6, 7, 8]

out = cp.octagon_only(cp.connecting(triangulation, curve),edges)

print(out)