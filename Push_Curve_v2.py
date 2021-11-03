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
from System import Guid
import clr
import System

t1 = [p[0] for p in points]
t2 = [p[1] for p in points]
newcurves = []
main_curve = master_curve
main_curve.Domain = rc.Geometry.Interval(0,1)


eps = epsilon
for i in range(len(t1)):
    t1paramnew = []
    t2paramnew = []
    t1param = main_curve.ClosestPoint(t1[i])[1]
    t2param = main_curve.ClosestPoint(t2[i])[1]
    #t1param = rs.CurveClosestPoint(main_curve, t1[i], segment_index=-1)
    #t2param = rs.CurveClosestPoint(main_curve, t2[i], segment_index=-1)
    if t1param > t2param:
        t1paramnew.append(t1param)
        t1paramnew.append(0)
        t2paramnew.append(1)
        t2paramnew.append(t2param)
    else:
        t1paramnew.append(t1param)
        t2paramnew.append(t2param)
    subcrvs = []
    for i in range(len(t1paramnew)):
        subcrv = main_curve.Trim(t1paramnew[i], t2paramnew[i])
        #subcrv = rs.AddSubCrv(main_curve, t1paramnew[i], t2paramnew[i])
        subcrvs.append(subcrv)
    if len(subcrvs) > 1:
        subcurve = rc.Geometry.Curve.JoinCurves(subcrvs)
        #subcurve = rs.JoinCurves(subcrvs)
        assert len(subcurve) == 1
        subcurve = subcurve[0]
    else:
        subcurve = subcrvs[0]
    #subcurve = rs.coercecurve(subcurve)
    subcurve.Domain=rc.Geometry.Interval(0,1)
    newpts = []
    """Need to specify num_of_seg"""
    length = rc.Geometry.Curve.GetLength(subcurve)
    #length = rs.CurveLength(subcurve)
    num_of_seg = int(length/div_space)
    divparams = subcurve.DivideByCount(num_of_seg,True)
    #divparams = rs.DivideCurve(subcurve, num_of_seg, create_points=False, return_points=False)

    for j in range(len(divparams)):
        divpt = subcurve.PointAt(divparams[j])

        #divpt = rs.EvaluateCurve(subcurve, divparams[j])
        
        cl_point_out = clr.StrongBox[rc.Geometry.Point3d]()
        ci_out = clr.StrongBox[rc.Geometry.ComponentIndex]()
        u_out = clr.StrongBox[System.Double]()
        v_out = clr.StrongBox[System.Double]()
        max_dist = 0
        normal = clr.StrongBox[rc.Geometry.Vector3d]()
        success = surface.ClosestPoint(divpt,cl_point_out, ci_out, u_out, v_out, max_dist, normal)
        normal = normal.Value
        
        #normal = rs.BrepClosestPoint(surface, divpt)[3]
        """Need to specify tangent"""
        tangent = subcurve.DerivativeAt(divparams[j],1)[1]
        #tangent = rs.CurveTangent(subcurve, divparams[j], segment_index=-1)
        pushoff = rc.Geometry.Vector3d.CrossProduct(tangent,normal)
        #pushoff = rs.VectorCrossProduct(tangent, normal)

        if j <= 20:
            dist = (eps*j)/20
        elif len(divparams)-j <= 20:
            dist = (eps*((len(divparams)-j-1)))/20
        else:
            dist = eps
        _ = pushoff.Unitize()
        #dist = eps * (len(divparams) / 2 - abs(len(divparams) / 2 - j - 1))
        pushoff_scaled = rc.Geometry.Vector3d.Multiply(pushoff,dist)

        newpt = rc.Geometry.Point3d.Add(divpt,pushoff_scaled)

        #newpt = rs.PointAdd(divpt, rs.VectorScale(pushoff, dist))
        if (j != 0) and (j!= len(divparams)-1):
            newpt = surface.ClosestPoint(newpt)
        
        #newpt = rs.BrepClosestPoint(surface, newpt)[0]
        newpts.append(newpt)
        
    newcrv = rc.Geometry.Curve.CreateInterpolatedCurve(newpts,3)
    #newcrv = rs.AddInterpCurve(newpts)
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
        subcrv = main_curve.Trim(t1paramnew[i], t2paramnew[i])
        #subcrv = rs.AddSubCrv(main_curve, t1paramnew[i], t2paramnew[i])
        subcrvs.append(subcrv)

    if len(subcrvs) > 1:
        subcurve2 = rc.Geometry.Curve.JoinCurves(subcrvs,.00000001,False)
        #subcurve2 = rs.JoinCurves(subcrvs)
        assert len(subcurve2) == 1
        subcurve2 = subcurve2[0]
    else:
        subcurve2 = subcrvs[0]

    newcrv.Domain = rc.Geometry.Interval(0,1)
    subcurve2.Domain = rc.Geometry.Interval(0,1)
    main_curve = rc.Geometry.Curve.JoinCurves([newcrv,subcurve2],.0000001,False)

    #main_curve = rs.JoinCurves([newcrv, subcurve2])

    assert len(main_curve) == 1
    main_curve = main_curve[0]
    #main_curve_coerced = rs.coercecurve(main_curve)
    main_curve.Domain = rc.Geometry.Interval(0,1)

    # need to make sure the main_curve is still oriented counter-clockwise around
    # the octagon. To do this we'll compare it's orientation to the orientation of 
    # subcurve2.
    p = subcurve2.PointAt(0)
    #p = rs.EvaluateCurve(subcurve2,0)

    t = main_curve.ClosestPoint(p)[1]
    #t = rs.CurveClosestPoint(main_curve,p)

    _ = main_curve.ChangeClosedCurveSeam(t)
    main_curve.Domain = rc.Geometry.Interval(0,1)
    #_ = rs.CurveSeam(Guid(main_curve),t)
    q = main_curve.LengthParameter(1)[1]

    q = rs.CurveArcLengthPoint(main_curve,1)
    p = rs.CurveArcLengthPoint(subcurve2,1)
    if not rs.PointCompare(p,q,tolerance=.01):
        _ = main_curve.Reverse()
        main_curve.Domain = rc.Geometry.Interval(0,1)
    """Reevaluate main_curve here?"""
    #rs.JoinCurves

#rs.AddInterpCurve(points, degree=3, knotstyle=0, start_tangent=None, end_tangent=None)
#rs.BrepClosestPoint(object_id, point)

