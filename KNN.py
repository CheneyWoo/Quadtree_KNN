#!/usr/bin/python
# -*- coding: utf-8 -*-
import Quadtree as qt
import math
import Queue
import time

start=time.clock()

def Pdist(point1, point2):
    return math.sqrt((point1.x-point2.x)**2 + (point1.y-point2.y)**2)

def dist(x1, x2, y1, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def MINDIST(root, q):
    if root.x0 <= q.x <= root.x0 + root.get_width() and  root.y0 <= q.y <= root.y0 + root.get_height():
        return 0
    elif (q.x < root.x0 or q.x > root.x0 + root.get_width()) and root.y0 <= q.y <= root.y0 + root.get_height():
        return abs(root.x0 - q.x)
    elif root.x0 <= q.x <= root.x0 + root.get_width() and (q.y < root.y0 or q.y > root.y0 + root.get_height()):
        return abs(root.y0 - q.y)
    elif q.x < root.x0 and q.y < root.y0:
        return dist(q.x, root.x0, q.y, root.y0)
    elif q.x < root.x0 and q.y > root.y0 + root.get_height():
        return dist(q.x, root.x0, q.y, root.y0 + root.get_height())
    elif q.x > root.x0 + root.get_width() and q.y < root.y0:
        return dist(q.x, root.x0 + root.get_width(), q.y, root.y0)
    elif q.x > root.x0 + root.get_width() and q.y > root.y0 + root.get_height():
        return dist(q.x, root.x0 + root.get_width(), q.y, root.y0 + root.get_height())

class Candidate():
    def __init__(self, point, distance):
        self.point = point
        self.distance = distance

quadtree = qt.QuadTree(200, qt.lon, qt.lat)
quadtree.subdivide()

def KNN(k, q):
    count = k
    KNN = []
    distances = []
    PriorityQueue = Queue.Queue()
    PriorityQueue.put(quadtree.root)
    while not PriorityQueue.empty():
        CurrentNode = PriorityQueue.get()
        if k == 0 and MINDIST(CurrentNode, q) > max(distances):
            break
        elif [CurrentNode] == (qt.find_children(CurrentNode)):
           for point in CurrentNode.points:
               if k > 0:
                   KNN += [Candidate(point, Pdist(point, q))]
                   k -= 1
                   distances += [Pdist(point, q)]
               elif Pdist(point, q) < max(distances):
                   for i in range(k):
                       if KNN[i].distance == max(distances):
                           KNN[i] = Candidate(point, Pdist(point, q))
                       if distances[i] == max(distances):
                           distances[i] = Pdist(point, q)
        else:
            for child in (qt.find_children(CurrentNode)):
                PriorityQueue.put(child)
    distances.sort()
    #print distances
    for e in range(count):
        print "point" + str(e) + ": " + str(distances[e])
        print str(KNN[e].point.x) + "," + str(KNN[e].point.y)

q = qt.Point(33.74140167236328,-118.40245056152344)
#KNN(4, q)

distance2 = []
#print len(quadtree.points)
for num in range(len(quadtree.points)):
    distance2 += [Pdist(q, quadtree.points[num])]
distance2.sort()
for num in range(10):
    print distance2[num]

end=time.clock()
print("Run time: ",end-start)