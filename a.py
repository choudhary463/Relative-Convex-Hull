from functools import cmp_to_key
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import random
import matplotlib.font_manager as fm
from matplotlib.cm import get_cmap
import addcopyfighandler

INT_MAX = 10000000

def random_point():
    return random.random()*random.randint(1,10)

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

def chk(i1, i2, n):
    if(i1 > i2):
        if(i1 != n - 1):
            return True
        else:
            if(i2 == 0):
                return False
            else:
                return True
    else:
        if(i1 + 1 != i2):
            return True
        else:
            return False

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

def random_polygon(n):
    arr = []
    for i in range(n):
        p = []
        for j in range(2):
            p.append(random_point())
        arr.append(p)
    return sort_points(arr)

def split(arr, points, closed):
    x = []
    y = []
    for p in arr:
        x.append(points[p[1]][p[0]][0])
        y.append(points[p[1]][p[0]][1])
    if(closed):
        x.append(points[arr[0][1]][arr[0][0]][0])
        y.append(points[arr[0][1]][arr[0][0]][1])
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

def print_polygon(rch, points, to_mark):
    Y1 = np.array(points[0])
    Y2 = np.array(points[1])
    Poly1 = Polygon(Y1, facecolor = 'k')
    Poly2 = Polygon(Y2, facecolor = 'r')
    if(len(to_mark)):
        if(type(to_mark[0][0]) is int):
            pts = []
            for p in to_mark:
                pts.append(points[p[1]][p[0]])
            to_mark = pts
    x,y = split(rch,points,True)
    line = plt.Line2D(x,y)

    plot1 = plt.figure(1)
    ax1 = plot1.add_subplot()
    ax1.add_patch(Poly2)
    ax1.add_patch(Poly1)
    ax1.add_line(line)
    for p in to_mark:
        plt.plot([p[0]], [p[1]], "-o", c='green')
    ax1.set_xlim([-15,150])
    ax1.set_ylim([-100,20])
    plt.axis('off')
    plt.show()
    exit(0)

def process_cavity(ch, points, i, iter):
    st = ch[i][0]
    type = ch[i][1]
    n = len(points[type])
    ne = i + 1
    en = ch[ne][0]
    poly = []
    poly2 = []
    j = st
    while(j != en):
        poly.append(points[type][j])
        poly2.append([j, type])
        j = (j + 1) % n
    poly.append(points[type][en])
    poly2.append([en, type])
    nch = []
    for k in range(len(points[type ^ 1])):
        p = points[type ^ 1][k]
        if(point_vs_polygon(poly, p) <= 0):
            nch.append([k, type ^ 1])
    nch.append(ch[i])
    nch.append(ch[ne])
    nch = convex_hull(nch, points)
    order = find_order(nch,ch[i],ch[i+1])
    order1 = []
    order2 = []
    if(len(order)):
        Os = []
        poly1 = []
        Os.append(ch[i])
        poly1.append(points[ch[i][1]][ch[i][0]])
        wh1 = order[0][0]
        t1 = order[0][1]
        l = len(points[t1])
        Os.append(order[0])
        poly1.append(points[t1][wh1])
        wh1 = (wh1 - 1 + l) % l
        Os.append([wh1,t1])
        poly1.append(points[t1][wh1])
        while(True):
            wh1 = (wh1 - 1 + l) % l
            if(point_vs_polygon(poly1, points[t1][wh1]) == 1):
                break
            else:
                Os.append([wh1,t1])
                poly1.append(points[t1][wh1])
        Oe = []
        poly2 = []
        Oe.append(ch[i + 1])
        poly2.append(points[ch[i+1][1]][ch[i+1][0]])
        wh2 = order[-1][0]
        Oe.append(order[-1])
        poly2.append(points[t1][wh2])
        wh2 = (wh2 + 1) % l
        Oe.append([wh2, t1])
        poly2.append(points[t1][wh2])
        while(True):
            wh2 = (wh2 + 1) % l
            if(point_vs_polygon(poly2 , points[t1][wh2]) == 1):
                break
            else:
                Oe.append([wh2, t1])
                poly2.append(points[t1][wh2])
        poly3 = []
        poly4 = []
        for k in range(len(points[type])):
            p = points[type][k]
            if(point_vs_polygon(poly1, p) < 0):
                poly3.append([k,type])
            if(point_vs_polygon(poly2, p) < 0):
                poly4.append([k,type])
        poly3.append(ch[i])
        poly3.append(order[0])
        poly4.append(order[-1])
        poly4.append(ch[i + 1])
        Is = convex_hull(poly3, points)
        Ie = convex_hull(poly4, points)
        order1 = find_order(Is, ch[i], order[0])
        order2 = find_order(Ie, order[-1], ch[i+1])

    nw = []
    for k in range(len(ch)):
        nw.append(ch[k])
        if(k == i):
            for p in order1:
                nw.append(p)
            for p in order:
                nw.append(p)
            for p in order2:
                nw.append(p)
    ch.clear()
    for p in nw:
        ch.append(p)

def relative_convex_hull(points):
    n1 = len(points[0])
    inner = []
    for i in range(n1):
        inner.append([i,0])

    ch = convex_hull(inner, points)
    i = 0
    s = len(ch)
    tt = 0
    iter = 0
    while(i < s - 1):
        if(ch[i][1] == ch[i + 1][1] and chk(ch[i][0], ch[i + 1][0] , len(points[ch[i][1]]))):
            process_cavity(ch, points, i, iter)
            iter += 1
            s = len(ch)
        i += 1
        tt += 1
    return ch

n = 5
points = test1()

rch = relative_convex_hull(points)
# print_polygon(rch, points, [])
