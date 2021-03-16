# CodeSkulptor runs Python programs in your browser.
# Click the upper left button to run this simple demo.

# CodeSkulptor is tested to run in recent versions of
# Chrome, Firefox, and Safari.

def abs_side(side):
    if side < 0:
        new_side = -1 - side
    else:
        new_side = side
    return new_side

def num_of_connections_within_a_triangle(triangle, intersection):
    num_of_connections = {}
    a = intersection[abs_side(triangle[0])]
    b = intersection[abs_side(triangle[1])]
    c = intersection[abs_side(triangle[2])]
    num_of_connections[(triangle[0], triangle[1])] = (a + b - c)/2
    num_of_connections[(triangle[2], triangle[0])] = (a + c - b)/2
    num_of_connections[(triangle[1], triangle[2])] = (b + c - a)/2
    return num_of_connections

def leaving_position(enteringp, triangle, intersection):
    "Enter a point; return the position at which it leaves the triangle."
    "The three sides of the triangle must be arranged in counterclockwise order."
    noc = num_of_connections_within_a_triangle(triangle, intersection)
    for i in range(0, 3):
        if triangle[i] == enteringp[0] or triangle[i] == -1-enteringp[0]:
            sidea = triangle[(i+1)%3]
            sideb = triangle[(i-1)%3]
            side = triangle[i]
    "Now consider all the possible situations. i.e., the possible orientations of the sides."
    if side < 0:
        if enteringp[1] < noc[(side, sidea)]:
            if sidea < 0:
                pos = intersection[abs_side(sidea)] - enteringp[1] - 1
            else:
                pos = enteringp[1]
            leavingp = (abs_side(sidea), pos)
        else:
            if sideb < 0:
                pos = intersection[abs_side(side)] - enteringp[1] - 1
            else:
                pos = intersection[abs_side(sideb)] - intersection[abs_side(side)] + enteringp[1]
            leavingp = (abs_side(sideb), pos)
    else:
        if enteringp[1] < noc[(sideb, side)]:
            if sideb < 0:
                pos = enteringp[1]
            else:
                pos = intersection[abs_side(sideb)] - enteringp[1] - 1
            leavingp = (abs_side(sideb), pos)
        else:
            if sidea < 0:
                pos = intersection[abs_side(sidea)] - intersection[abs_side(side)] + enteringp[1]
            else:
                pos = intersection[abs_side(side)] - enteringp[1] - 1
            leavingp = (abs_side(sidea), pos)
    return leavingp
   
def connecting(triangulation, intersection):
    connection = []
    for i in range(0,9):
        if intersection[i] > 0:
            entersd = i
            break
    for tr in triangulation:
        for i in range(0,3):
            if entersd == tr[i]:
                entertr = tr
                break
    enterp = (entersd, 0)
    count = 0
    while count < 1:
        leavingp = leaving_position(enterp, entertr, intersection)
        connection.append((enterp, leavingp))
        enterp = leavingp
        #print(leavingp)
        for tr in triangulation:
            for i in range(0,3):
                if leavingp[0] == tr[i] or leavingp[0] == -1-tr[i]:
                    if tr != entertr:
                        entertr0 = tr
                        #print(entertr)
        entertr = entertr0
        if enterp == (entersd, 0):
            count = count + 1
    return connection    

def octagon_only(connection, edges):
    octagon_con = []
    "Connection is the result from the connecting function."
    "Edges is a list of sides that are the sides of the octagon."
    "In the flipper default case, edges = [1, 6, 7, 8]."
    for i in range(0,len(connection)):
        if connection[i][0][0] in edges:
            for j in range(i, len(connection)):
                if connection[j][1][0] in edges:
                    octagon_con.append((connection[i][0], connection[j][1]))
                    break
    "The last tuple that connects back to the starting point may not be included, so we add it here."
    if connection[0][0][0] not in edges:
        octagon_con.append((octagon_con[len(octagon_con)-1][1], octagon_con[0][0]))
    return octagon_con


"triangulation = [(-9, -2, -1), (-8, 8, 3), (-7,-3,7), (-6,6,2), (-5,-4,5), (0,4,1)]"
"""def connecting_points(intersection, triangulation):
    connection = {}
    noc = []
    for triangle in triangulation:
        noc.append(num_of_connections_within_a_triangle(triangle, intersection))
    connection[(-9,1)] = min(noc[5][(0,1)], noc[0][(-9,-1)])
    connection[(-9,-2)] = noc[0][(-9,-2)]
    connection[(-2,1)] = noc[5][(0,1)] - connection[(-9,1)]
    connection[(-7,7)] = noc[2][(-7,7)]
    connection[(6,7)] = min(noc[3][(-6,2)], noc[2][(-3,7)])
    connection[(-7,6)] = noc[3][(-6,2)] - connection[(6,7)]
    connection[(-8,8)] = noc[1][(-8,8)]
    connection[(-7,1)] = min(noc[5][(4,1)], noc[4][(-5,5)], noc[3][(-6,2)], noc[2][(-7,-3)])"""
        

"Start with a point on 0 or 1 or 2 or 3 that has no point on one side of it"
"Consider a triangle it is in"
"Compare its serial number, which is initially 0, to the num_of_connections of the side its on and the other two sides"
"By this we can tell which side it is going to"
"If we reach a side that we have encountered before, serial number + 1"
"Repeat until the serial number on the starting edge exceeds the boundary"

"Another method: point to point"
"iteration: start from, for example, (1,0), (1,0) to (0,0), ... Stop and record at edges on the side."
"[((1,0),(~8,0)), ...]"

if __name__ == "__main__":
    
    
    triangulation = [(~1, ~8, ~0), (~7, 3, 8), (~2, ~6, 7), (~5, 2, 6), (~3, ~4, 5), (0, 1, 4)]
    intersection1 = [1, 0, 1, 0, 1, 1, 0, 1, 1]
    intersection2 = [2, 1, 1, 0, 1, 1, 0, 1, 1]
    intersection3 = [0, 1, 0, 1, 1, 0, 0, 0, 1]
    print(connecting(triangulation, intersection1))
    print(connecting(triangulation, intersection2))
    print(connecting(triangulation, intersection3))
    edges = [1, 6, 7, 8]
    print(octagon_only(connecting(triangulation, intersection3), edges))
    print(octagon_only(connecting(triangulation, intersection2), edges))
    print(octagon_only(connecting(triangulation, intersection1), edges))







