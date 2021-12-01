"""Provides a scripting component.
    Inputs:
        mapCurveList: An ordered list of rhino curves
        abstractPointsList: A list of numbered intersections with each map edge, 
            as processed by flipper
    Output:
        pairedPushPoints3D: A list of pairs of 3d points corresponding to the 
            intersection points indicated in the abstractPointsList"""

__author__ = "Shoon"
__version__ = "2021.03.26"

import rhinoscriptsyntax as rs

# Count the number of intersection points on each edge.
# This will tell us how we should space them out.
pointsPerEdge = {}

for pair in abstractPointsList:
    for intersection in pair:
        if (intersection[0] not in pointsPerEdge.keys()):
            pointsPerEdge[intersection[0]] = 1
        else:
            pointsPerEdge[intersection[0]] += 1

# Place the points on each curve, limited to the parameter range [0.1, 0.9].
# Staying away from where we meet the puncture curves is a little safer.
pairedPushPoints3D = []
GH_pairedPushPoints3D = []

for pair in abstractPointsList:
    firstParam = (0.8 * (pair[0][1]/pointsPerEdge[pair[0][0]])) + 0.1
    secondParam = (0.8 * (pair[1][1]/pointsPerEdge[pair[1][0]])) + 0.1
    
    curve_index1 = pair[0][0]
    if curve_index1 < 4:
        first = rs.EvaluateCurve(mapCurveList[pair[0][0]], firstParam)
    else:
        print(curve_index1,curve_index1%4)
        first = rs.EvaluateCurve(mapCurveList[curve_index1 % 4], firstParam)
        first  = rs.EvaluateCurve(mapCurveList[curve_index1], rs.CurveClosestPoint(mapCurveList[curve_index1], first))
        
    curve_index2 = pair[1][0]
    if curve_index2 < 4:
        second = rs.EvaluateCurve(mapCurveList[pair[1][0]], secondParam)
    else:
        print(curve_index2,curve_index2%4)
        second = rs.EvaluateCurve(mapCurveList[curve_index2 % 4], secondParam)
        second  = rs.EvaluateCurve(mapCurveList[curve_index2], rs.CurveClosestPoint(mapCurveList[curve_index2], second))
        
    pairedPushPoints3D.append((first, second))
    GH_pairedPushPoints3D.append(first)
    GH_pairedPushPoints3D.append(second)
    
pairedPushPoints3D = pairedPushPoints3D
print(pairedPushPoints3D)