# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 18:20:42 2019

@author: Rens
"""
from random import randint
from math import sqrt
import matplotlib.pyplot as plt

def firstRandomClusters(points,k):
    randomClusters = []
    copyPoints = points.copy()
    for i in range(k):
        
        totalPoints = len(copyPoints)-1
        removePoint = randint(0,totalPoints)
        randomClusters.append(copyPoints[randint(0,totalPoints)])
        copyPoints.remove(copyPoints[removePoint])

        
    return randomClusters


def assignPoints(points,centers):
    pointsAssign = []
    
    for i in range(len(points)):
        minVar = float("inf")
        goodCenter = 0
        for j in range(len(centers)):
            distCenter = distanceBetweenPoints(points[i],centers[j])
            if minVar > distCenter:
                minVar = distCenter
                goodCenter = j
        pointsAssign.append(goodCenter)
    return pointsAssign

def distanceBetweenPoints(pointA,pointB):
    
    if (len(pointA) != len(pointB)):
        print(pointA)
        print(pointB)
        print("The dimensions are wrong here")        
        

    numberOfDimensions = len(pointA)
    totalSum = 0
    for i in range(numberOfDimensions):
        squareRoot = (pointA[i]-pointB[i]) **2
        totalSum += squareRoot
    
    return sqrt(totalSum)

def meanOfListOfPoints(points):
    meanPoint = []
   
    for dimension in range(len(points[0])):
        sumBefore = 0
        for point in points:
            sumBefore += point[dimension]
            
        meanPoint.append(sumBefore/len(points))
        
    return meanPoint

def updateClusterCenters(points,assigns,clusters):
    pointsPerCluster = []
    
    for cluster in range(len(clusters)):
        pointsPerCluster.append([])
        clusterPoints = [points[index] for index, value in enumerate(assigns) if value == cluster]
        pointsPerCluster[cluster] = clusterPoints
        if len(clusterPoints)>0:
            x, y = zip(*clusterPoints)
            plt.scatter(x,y,color="C"+str(cluster))

        x, y = zip(*clusters)
        plt.scatter(x,y,marker="+",color="red",s=100)
    plt.show()  
    for i in range(len(pointsPerCluster)):
       
        if(len(pointsPerCluster[i])>0):
          clusters[i] = meanOfListOfPoints(pointsPerCluster[i])
        
def kpoints(points,k,maxRuns = 100):
    clusters = firstRandomClusters(points,k)
    newAssignments = assignPoints(points,clusters)
    oldAssignments = None
    runs = 0
    while (runs != maxRuns and oldAssignments != newAssignments):
        oldAssignments=newAssignments
        updateClusterCenters(points,newAssignments,clusters)
        
        newAssignments = (assignPoints(points,clusters))
        runs += 1
    
    
    return newAssignments

 
       
points = [[105,197],[193,11],[156,116],[166,44],[63,162],[86,71],[174,25],[174,131],[5,24],[52,59],[129,84],[148,191],[14,151],[90,30],[140,102],[53,92],[98,175],[70,47],[43,200],[185,25],[155,184],[46,36],[155,64],[182,19],[63,158],[122,189],[196,41],[141,161],[99,45],[168,99],[36,85],[102,29],[50,19],[148,178],[61,38],[74,144],[138,40],[109,170],[164,93],[162,36],[58,122],[11,88],[146,183],[191,172],[81,13],[89,22],[175,138],[71,113],[160,87],[172,61],[182,109],[8,198],[166,139],[117,121],[38,33],[53,21],[187,127],[97,85],[35,78],[19,175],[147,33],[12,138],[122,74],[33,143],[119,19],[179,139],[111,65],[138,53],[97,63],[189,121],[23,38],[155,130],[88,46],[13,29],[47,75],[2,122],[65,65],[106,170],[14,98],[80,161],[58,164],[87,32],[129,110],[71,133],[1,34],[143,70],[114,24],[66,79],[91,12],[103,94],[44,197],[47,24],[10,127],[119,12],[190,85],[170,177],[4,93],[185,159],[181,117],[84,125],[102,163],[30,87],[18,97],[91,81],[165,12],[3,118],[63,176],[103,197],[152,165],[100,193],[161,83],[81,40],[2,164],[47,129],[160,6],[64,89],[97,176],[181,189]
]



assigns = kpoints(points,3)