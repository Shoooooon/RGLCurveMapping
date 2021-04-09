

## this is a python executable that will be called from GH to get curve data using Connecting_Points.py


import Connecting_Points_0409 as cp

from sys import argv

script, curve = argv

curve = [int(c) for c in curve]

triangulation = [(~1, ~8, ~0), (~7, 3, 8), (~2, ~6, 7), (~5, 2, 6), (~3, ~4, 5), (0, 1, 4)]
edges = [1, 6, 7, 8]

out = cp.octagon_only(cp.connecting(triangulation, curve),edges)

D = {1:3, -2:7, 6:1, -7:5, 7:2, -8:6, 8:0, -9:4}


new_out = []
for tup in out:
	new_tup = ((D[tup[0][0]], tup[0][1]),(D[tup[1][0]], tup[1][1]))
	new_out.append(new_tup)




print(new_out)