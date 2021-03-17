

## this is a python executable that will be called from GH to get curve data using Connecting_Points.py


import Connecting_Points as cp

from sys import argv
import flipper

script, init_curve, mapping_class, iterations = argv



triangulation = [(~1, ~8, ~0), (~7, 3, 8), (~2, ~6, 7), (~5, 2, 6), (~3, ~4, 5), (0, 1, 4)]
edges = [1, 6, 7, 8]

S = flipper.load('S_2_1')

h = S.mapping_class(mapping_class)

curve = S.lamination(init_curve)

for i in range(int(iterations)):
	curve = h(curve)


out = cp.octagon_only(cp.connecting(triangulation, curve.geometric),edges)
#out = cp.connecting(triangulation, curve.geometric)

print(out)