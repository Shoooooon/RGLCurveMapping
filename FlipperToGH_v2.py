

## this is a python executable that will be called from GH to get curve data using Connecting_Points.py


import Connecting_Points_0409 as cp
import Reordering_points as rp

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
out = rp.reorder_list(out)

D = {1:3, -2:7, 6:1, -7:5, 7:2, -8:6, 8:0, -9:4}

new_out = []
for tup in out:
	new_tup = ((D[tup[0][0]], tup[0][1]),(D[tup[1][0]], tup[1][1]))
	new_out.append(new_tup)


print(new_out)