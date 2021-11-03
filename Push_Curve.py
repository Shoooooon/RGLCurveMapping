__author__ = "danielqiu"

"""
Input: t1: a list of 3D points that are the starting points of connections.
       t2: a list of 3D points that are the ending points of connections.
       main_curve
       surface
       eps
Output:
"""
import rhinoscriptsyntax as rs
import Rhino as rc

t1 = [p[0] for p in points]
t2 = [p[1] for p in points]
newcurves = []

eps = 0.01
for i in range(len(t1)):
    t1paramnew = []
    t2paramnew = []
    t1param = rs.CurveClosestPoint(main_curve, t1[i], segment_index=-1)
    t2param = rs.CurveClosestPoint(main_curve, t2[i], segment_index=-1)
    if t1param > t2param:
        t1paramnew.append(t1param)
        t1paramnew.append(0)
        t2paramnew.append(1)
        t2paramnew.append(t2param)
    else:
        t1paramnew.append(t1param)
        t2paramnew.append(t2param)
    num_of_seg = 100
    subcrvs = []
    for i in range(len(t1paramnew)):
        subcrv = rs.AddSubCrv(main_curve, t1paramnew[i], t2paramnew[i])
        subcrvs.append(subcrv)
    if len(subcrvs) > 1:
        subcurve = rs.JoinCurves(subcrvs)
        assert len(subcurve) == 1
        subcurve = subcurve[0]
    else:
        subcurve = subcrvs[0]
    newpts = []
    """Need to specify num_of_seg"""
    divparams = rs.DivideCurve(subcurve, num_of_seg, create_points=True, return_points=False)
    print(divparams)
    for j in range(len(divparams)):
        divpt = rs.EvaluateCurve(main_curve, divparams[j])
        normal = rs.BrepClosestPoint(surface, divpt)[3]
        """Need to specify tangent"""
        tangent = rs.CurveTangent(main_curve, divparams[j], segment_index=-1)
        pushoff = rs.VectorCrossProduct(tangent, normal)
        dist = eps * (len(divparams) / 2 - abs(len(divparams) / 2 - j - 1))
        newpt = rs.PointAdd(divpt, rs.VectorScale(pushoff, dist))
        newpt = rs.BrepClosestPoint(surface, newpt)[0]
        newpts.append(newpt)
    newcrv = rs.AddInterpCurve(newpts)
    newcurves.append(newcrv)
    t1paramnew = []
    t2paramnew = []
    if t1param < t2param:
        t1paramnew.append(t2param)
        t1paramnew.append(0)
        t2paramnew.append(1)
        t2paramnew.append(t1param)
    else:
        t1paramnew.append(t2param)
        t2paramnew.append(t1param)
    subcrvs = []
    for i in range(len(t1paramnew)):
        subcrv = rs.AddSubCrv(main_curve, t1paramnew[i], t2paramnew[i])
        subcrvs.append(subcrv)
    if len(subcrvs) > 1:
        subcurve2 = rs.JoinCurves(subcrvs)
        assert len(subcurve2) == 1
        subcurve2 = subcurve2[0]
    else:
        subcurve2 = subcrvs[0]
    print(t1paramnew)
    print(t2paramnew)
    print(subcurve)
    print(subcurve2)
    print(main_curve)
    main_curve = rs.JoinCurves([subcurve, subcurve2])
    assert len(main_curve) == 1
    main_curve = main_curve[0]
    print(main_curve)
    main_curve.Domain = rc.Geometry.Interval(0,1)
    """Reevaluate main_curve here?"""
    #rs.JoinCurves

#rs.AddInterpCurve(points, degree=3, knotstyle=0, start_tangent=None, end_tangent=None)
#rs.BrepClosestPoint(object_id, point)