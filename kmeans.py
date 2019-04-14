# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 18:20:42 2019

@author: Rens
"""
from random import randint
from math import sqrt
import matplotlib.pyplot as plt

def firstRandomClusters(points,k):
    """
    Select K random points to work as cluster centers
    """
    
    
    randomClusters = []
    copyPoints = points.copy()
    for i in range(k):
        
        totalPoints = len(copyPoints)-1
        removePoint = randint(0,totalPoints)
        randomClusters.append(copyPoints[randint(0,totalPoints)])
        copyPoints.remove(copyPoints[removePoint])

        
    return randomClusters


def assignPoints(points,centers,mustLinkConstraints,cannotLinkConstraints):
    """
    Assign each point to the closest cluster, without breaking constraints.
    """
    
    pointsAssign = []
    assignedPoints = []
    pointsPerCluster = []
    for cluster in range(len(centers)):
        pointsPerCluster.append([])
    
    for i in range(len(points)):
        minVar = float("inf")
        goodCenter = 0
        assignedPoint =False
        for j in range(len(centers)):
            distCenter = distanceBetweenPoints(points[i],centers[j])
            if minVar > distCenter and not violateConstraints(points[i],pointsPerCluster[j],mustLinkConstraints,cannotLinkConstraints,assignedPoints):
                minVar = distCenter
                goodCenter = j
                pointsPerCluster[j].append(points[i])
                assignedPoints.append(points[i])
                assignedPoint = True
                
        if not assignedPoint:
            print("failed")
            return False
        pointsAssign.append(goodCenter)
    return pointsAssign

def distanceBetweenPoints(pointA,pointB):
    """
    Calculate the Euclidian distance between two points.
    """
    
    
    if (len(pointA) != len(pointB)):
        print(pointA)
        print(pointB)
        print("The dimensions are wrong here")        
        return "ERROR"

    numberOfDimensions = len(pointA)
    totalSum = 0
    for i in range(numberOfDimensions):
        squareRoot = (pointA[i]-pointB[i]) **2
        totalSum += squareRoot
    
    return sqrt(totalSum)

def meanOfListOfPoints(points):
    """
    Input is an array of points. We find the mean for each dimension. Output is a single point.
    """
    
    meanPoint = []
   
    for dimension in range(len(points[0])):
        sumBefore = 0
        for point in points:
            sumBefore += point[dimension]
            
        meanPoint.append(sumBefore/len(points))
        
    return meanPoint

def updateClusterCenters(points,assigns,clusters,draw=False):
    """
    Old clusters centers go in. New assignments go in. All the points of the dataset go in.
    If draw is True we draw the current partition.
    """
    
    pointsPerCluster = []
    
    for cluster in range(len(clusters)):
        pointsPerCluster.append([])
        clusterPoints = [points[index] for index, value in enumerate(assigns) if value == cluster]
        pointsPerCluster[cluster] = clusterPoints
        
        if draw:
            if len(clusterPoints)>0:
                x, y = zip(*clusterPoints)
                plt.scatter(x,y,color="C"+str(cluster))
    
            x, y = zip(*clusters)
            plt.scatter(x,y,marker="+",color="red",s=100)
    if draw:
        plt.show()
        
    for i in range(len(pointsPerCluster)):
       
        if(len(pointsPerCluster[i])>0):
          clusters[i] = meanOfListOfPoints(pointsPerCluster[i])

def violateConstraints(newPoint,pointsInCluster,mustLinkConstraints,cannotLinkConstraints,alreadyAssignedPoints):
    """
    Checks if a newPoints has a mustlink constraint. If it does it checks if the point it needs to be linked to is already assigned in a cluster. If it is check if is in this cluster. If it is continue, else return true.
    After that check if cannot link constraint in a cluster is violated.
    """
    
    
    for constraint in mustLinkConstraints:
        found = False
        if constraint[0] == newPoint:
            if constraint[1] in alreadyAssignedPoints:
                if constraint[1] in pointsInCluster:
                        found = True
                if not found:
                    return True
        if constraint[1] == newPoint:
            if constraint[0] in alreadyAssignedPoints:
                if constraint[0] in pointsInCluster:
                        found = True
                if not found:
                    return True
        

    for constraint in cannotLinkConstraints:
        foundCannot = False
        if constraint[0] == newPoint:
            for point in pointsInCluster:               
                if constraint[1] == point:
                    foundCannot = True
        if constraint[1] == newPoint:
            for point in pointsInCluster:               
                if constraint[1] == point:
                    foundCannot = True
        if foundCannot:
            return True
    
    return False
        
def kpoints(points,k,maxRuns = 100,draw=False,mustLinkConstraints = [],cannotLinkConstraints = []):
    """
    Main function, Points and K are not optional. MaxRuns and draw are optional.
    MaxRuns is the total number of iterations the algorithm is allowed to do.
    If draw is True the algorithm will output the plot of each iteration.
    """
    
    clusters = firstRandomClusters(points,k)
    newAssignments = assignPoints(points,clusters,mustLinkConstraints,cannotLinkConstraints)
    oldAssignments = None
    runs = 0
    
    while (runs != maxRuns and oldAssignments != newAssignments):
        oldAssignments=newAssignments
        updateClusterCenters(points,newAssignments,clusters,draw)
        
        newAssignments = (assignPoints(points,clusters,mustLinkConstraints,cannotLinkConstraints))
        runs += 1
    
    
    return newAssignments

 
       
#points = [[105,197],[193,11],[156,116],[166,44],[63,162],[86,71],[174,25],[174,131],[5,24],[52,59],[129,84],[148,191],[14,151],[90,30],[140,102],[53,92],[98,175],[70,47],[43,200],[185,25],[155,184],[46,36],[155,64],[182,19],[63,158],[122,189],[196,41],[141,161],[99,45],[168,99],[36,85],[102,29],[50,19],[148,178],[61,38],[74,144],[138,40],[109,170],[164,93],[162,36],[58,122],[11,88],[146,183],[191,172],[81,13],[89,22],[175,138],[71,113],[160,87],[172,61],[182,109],[8,198],[166,139],[117,121],[38,33],[53,21],[187,127],[97,85],[35,78],[19,175],[147,33],[12,138],[122,74],[33,143],[119,19],[179,139],[111,65],[138,53],[97,63],[189,121],[23,38],[155,130],[88,46],[13,29],[47,75],[2,122],[65,65],[106,170],[14,98],[80,161],[58,164],[87,32],[129,110],[71,133],[1,34],[143,70],[114,24],[66,79],[91,12],[103,94],[44,197],[47,24],[10,127],[119,12],[190,85],[170,177],[4,93],[185,159],[181,117],[84,125],[102,163],[30,87],[18,97],[91,81],[165,12],[3,118],[63,176],[103,197],[152,165],[100,193],[161,83],[81,40],[2,164],[47,129],[160,6],[64,89],[97,176],[181,189]]
#mustLinkConstraint = [[[105,197],[86,71]],[[105,197],[5,24]],[[105,197],[44,197]]]
#cannotLinkConstraint = [[52,59],[11,88],[[63,162],[86,71]]]
#kpoints(points,3,draw=True,mustLinkConstraints= mustLinkConstraint,cannotLinkConstraints=cannotLinkConstraint)