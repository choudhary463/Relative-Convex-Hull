from functools import cmp_to_key
from pickle import TRUE
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import random
import matplotlib.font_manager as fm
from matplotlib.cm import get_cmap
import addcopyfighandler

INT_MAX = 10000000

def orientation(p1, p2, p3):
    val = (p2[1]- p1[1]) * (p3[0] - p2[0]) - (p3[1]- p2[1]) * (p2[0] - p1[0])
    if(val < 0):
        return 1
    elif(val > 0):
        return -1
    return 0

def sort_points(arr, points):
    lmpi = 0
    n = len(arr)
    for i in range(n):
        cur_x = points[arr[i][1]][arr[i][0]][0]
        cur_y = points[arr[i][1]][arr[i][0]][1]
        prev_x = points[arr[lmpi][1]][arr[lmpi][0]][0]
        prev_y =points[arr[lmpi][1]][arr[lmpi][0]][1]
        if(cur_x < prev_x):
            lmpi = i
        elif (cur_x == prev_x and cur_y < prev_y) :
            lmpi = i
    left_most_point = arr[lmpi]
    arr.remove(arr[lmpi])
    angle = lambda p1, p2 : orientation(points[left_most_point[1]][left_most_point[0]], points[p1[1]][p1[0]], points[p2[1]][p2[0]])
    arr.sort(key = cmp_to_key(angle))
    res = [left_most_point]
    for p in arr:
        res.append(p)
    return res

def convex_hull(arr, points):
    arr = sort_points(arr, points)
    n = len(arr)
    res = []
    for p in arr:
        while (len(res) > 1 and orientation(points[res[-2][1]][res[-2][0]], points[res[-1][1]][res[-1][0]], points[p[1]][p[0]]) >=0) :
            res.pop()
        res.append(p)
    return res
    
def point_vs_polygon(arr, p):
    n = len(arr)
    if(n < 3):
        return 1
    tot = 0
    for i in range(n):
        if(p == arr[i]):
            return 0
        j = (i + 1) % n
        if(arr[i][1] == p[1] and arr[j][1] == p[1]):
            if(min(arr[i][0], arr[j][0]) <= p[0] and p[0] <= max(arr[i][0], arr[j][0])):
                return 0
        else:
            below = (arr[i][1] < p[1])
            if(below != (arr[j][1] < p[1])):
                type = orientation(p, arr[i], arr[j])
                if(type == 0):
                    return 0
                if(below == (type > 0)):
                    if(below):
                        tot = tot + 1
                    else:
                        tot = tot - 1
    if(tot == 0):
        return 1
    else:
        return -1

def polygon_vs_polygon(arr, arr2):
    for p in arr2:
        if(point_vs_polygon(arr, p) < 0):
            return False
    return True

def split(arr, points, closed):
    x = []
    y = []
    for p in arr:
        x.append(points[p[1]][p[0]][0])
        y.append(points[p[1]][p[0]][1])
    if(len(arr)):
        if(closed):
            x.append(points[arr[0][1]][arr[0][0]][0])
            y.append(points[arr[0][1]][arr[0][0]][1])
    return x,y

def split2(points):
    x = []
    y = []
    for p in points:
        x.append(p[0])
        y.append(p[1])
    if(len(points)):
        x.append(points[0][0])
        y.append(points[0][1])
    return x,y

def test1():
    innerx = [23.1,39.3,43.7,54.3,55.3,80.7,83.5,98.9,107.5,101.7,117.1,123.9,101.1,87.9,87.9,40.3,45.7,35.5,13.5]
    innery = [-21.3,-24.9,-46.9,-35.3,-51.9,-51.7,-20.7,-58.9,-47.9,-20.3,-13.7,-49.9,-71.7,-66.5,-56.3,-56.3,-69.7,-72.7,-36.7]
    outerx = [4.1,46.5,42.5,58.3,62.3,75.5,77.1,67.5,70.9,63.5,67.3,87.9,98.9,99.3,127.9,132.7,115.5,83.3,81.7,69.1,53.1,46.3,20.1]
    outery = [-29.3,-3.7,-40.7,-25.9,-46.1,-46.1,-21.9,-30.3,-37.9,-37.9,-2.3,-4.1,-39.7,-7.9,-14.7,-51.5,-76.5,-76.7,-63.3,-83.3,-60.9,-79.5,-76.9]
    arr1 = []
    arr2 = []
    l1 = len(innerx)
    l2 = len(outerx)
    for i in range(l1):
        p = [innerx[i], innery[i]]
        arr1.append(p)
    for i in range(l2):
        p = [outerx[i], outery[i]]
        arr2.append(p)
    res = []
    res.append(arr1)
    res.append(arr2)
    return res

def print_polygon(rch, points, new_points, triangle):
    Y1 = np.array(new_points[0])
    Y2 = np.array(new_points[1])
    Poly1 = Polygon(Y1, facecolor = 'k')
    Poly2 = Polygon(Y2, facecolor = 'r')
    x,y = split(rch,points,True)
    x1,y1 =  split2(triangle)
    line = plt.Line2D(x,y)
    line2 = plt.Line2D(x1,y1)
    plot1 = plt.figure(1)
    ax1 = plot1.add_subplot()
    ax1.add_patch(Poly2)
    ax1.add_patch(Poly1)
    ax1.add_line(line)
    ax1.add_line(line2)
    ax1.set_xlim([-15,150])
    ax1.set_ylim([-100,20])
    plt.axis('off')
    plt.show()
    exit(0)

def wut(prev, points, idx):
    res = []
    for i in range(len(points[idx])):
        if(prev[i] != -1):
            res.append(points[idx][i])
    return res

def remove_convex(outer, inner, points):
    other = []
    for p in inner:
        other.append(points[p[1]][p[0]])
    n = len(points[1])
    prev = [-1 for i in range(n)]
    next = [-1 for i in range(n)]
    vis = [False for i in range(n)]
    m = len(outer)
    tot = m
    visited = 0
    cur = outer[0][0]
    for i in range(m):
        prev[outer[i][0]] = outer[(i - 1 + m) % m][0]
        next[outer[i][0]] = outer[(i + 1) % m][0]
    while(visited < tot):
        if(vis[cur]):
            cur = next[cur]
            continue
        if(orientation(points[1][prev[cur]], points[1][cur], points[1][next[cur]]) < 0):
            if(polygon_vs_polygon([points[1][prev[cur]], points[1][cur], points[1][next[cur]]], other)):
                pr = prev[cur]
                ne = next[cur]
                prev[ne] = pr
                next[pr] = ne
                prev[cur] = -1
                next[cur] = -1
                if(vis[pr]):
                    visited -= 1
                if(vis[ne]):
                    visited -= 1
                vis[pr] = False
                vis[ne] = False
                cur = ne
                tot -= 1
            else:
                vis[cur] = True
                visited += 1
                cur = next[cur]
        else:
            vis[cur] = True
            visited += 1
            cur = next[cur]
    res = []
    visited = 0
    while(visited < tot):
        res.append([cur, 1])
        cur = next[cur]
        visited += 1
    return res

def remove_concave(inner, outer, points):
    other = []
    for p in outer:
        other.append(points[p[1]][p[0]])
    n = len(points[0])
    prev = [-1 for i in range(n)]
    next = [-1 for i in range(n)]
    vis = [False for i in range(n)]
    m = len(inner)
    tot = m
    visited = 0
    cur = inner[0][0]
    for i in range(m):
        prev[inner[i][0]] = inner[(i - 1 + m) % m][0]
        next[inner[i][0]] = inner[(i + 1) % m][0]
    while(visited < tot):
        if(vis[cur]):
            cur = next[cur]
            continue
        if(orientation(points[0][prev[cur]], points[0][cur], points[0][next[cur]]) > 0):
            if(polygon_vs_polygon([points[0][prev[cur]], points[0][cur], points[0][next[cur]]], other)):
                pr = prev[cur]
                ne = next[cur]
                prev[ne] = pr
                next[pr] = ne
                prev[cur] = -1
                next[cur] = -1
                if(vis[pr]):
                    visited -= 1
                if(vis[ne]):
                    visited -= 1
                vis[pr] = False
                vis[ne] = False
                cur = ne
                tot -= 1
            else:
                vis[cur] = True
                visited += 1
                cur = next[cur]
        else:
            vis[cur] = True
            visited += 1
            cur = next[cur]
    res = []
    visited = 0
    while(visited < tot):
        res.append([cur, 0])
        cur = next[cur]
        visited += 1
    return res

def find_order(ch, p1, p2):
    n = len(ch)
    i1 = -1
    i2 = -1
    order = []
    for k in range(n):
        if(ch[k] == p1):
            i1 = k
        elif(ch[k] == p2):
            i2  = k
        else:
            order.append(ch[k])
    if((i1 + 1) % n == i2):
        order.reverse()
    return order

def relative_convex_hull(points):
    inner = []
    outer = []
    for i in range(len(points[0])):
        inner.append([i,0])
    for i in range(len(points[1])):
        outer.append([i,1])
    
    outer = remove_convex(outer, inner, points)
    inner = remove_concave(inner, outer, points)

    n1 = len(inner)
    n2 = len(outer)
    res1 = []
    res2 = []
    for i in range(n1):
        pr = (i - 1 + n1) % n1
        ne = (i + 1) % n1
        if(orientation(points[0][inner[pr][0]], points[0][inner[i][0]], points[0][inner[ne][0]]) < 0):
            res1.append(inner[i])
    for i in range(n2):
        pr = (i - 1 + n2) % n2
        ne = (i + 1) % n2
        if(orientation(points[1][outer[pr][0]], points[1][outer[i][0]], points[1][outer[ne][0]]) > 0):
            res2.append(outer[i])
    res = []
    n3 = len(res1)
    n4 = len(points[0])
    for i in range(n3):
        pr = res1[i][0]
        ne = res1[(i + 1) % n3][0]
        poly = []
        while(pr != ne):
            poly.append(points[0][pr])
            pr = (pr + 1) % n4
        poly.append(points[0][ne])
        pts = []
        pts.append(res1[i])
        pts.append(res1[(i + 1) % n3])
        for p in res2:
            if(point_vs_polygon(poly, points[p[1]][p[0]]) < 0):
                pts.append(p)
        pts = convex_hull(pts, points)
        order = find_order(pts, res1[i], res1[(i + 1) % n3])
        res.append(res1[i])
        for p in order:
            res.append(p)
    new_points = [[] for _ in range(2)]
    for p in inner:
        new_points[p[1]].append(points[p[1]][p[0]])
    for p in outer:
        new_points[p[1]].append(points[p[1]][p[0]])
    return res, new_points

points = test1()

rch, new_points = relative_convex_hull(points)

print_polygon(rch,points,new_points,[])