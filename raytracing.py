import pygame
import sys
from pygame.locals import *
import numpy
WINDOWHEIGHT=300
WINDOWWIDTH=300
W=1.0
H=1.0
L=1.0

pygame.init()
RED=(255,0,0)
BACKGROUND=(255,255,255)

eye=numpy.array([0.0,0.0,0.0])
sphere={}
sphere["radius"]=1
sphere["center"]=numpy.array([0.0,0.0,3.0])
sphere["color"]=RED

lightSource={}
lightSource["center"]=numpy.array([1.5,1.5,1.0])


def convert(i,j):
    x= W/2-i/(WINDOWWIDTH-1)*W
    y= H/2-j/(WINDOWHEIGHT-1)*H
    z= L
    return numpy.array([x,y,z]) 

def rayTracing(i,j):
    screenPoint=convert(i,j)
    ray=screenPoint-eye 
    vecE=ray/numpy.linalg.norm(ray)
    point=screenPoint 
    isTouched=False
    for iteration in range(10):
        dist=distance(sphere,point)
        if dist<0.0:
            isTouched=True 
            break
        dist=max(0.001,dist)
        point=point+dist*vecE
    if isTouched:
        vecLight=lightSource["center"]-point
        vecLight=vecLight/numpy.linalg.norm(vecLight)
        vecSphere=point-sphere["center"]
        vecSphere=vecSphere/numpy.linalg.norm(vecSphere)
        cosA=vecLight[0]*vecSphere[0]+vecLight[1]*vecSphere[1]+vecLight[2]*vecSphere[2]
        light=0.3
        if cosA>0.0:
            light=min(light+cosA,1.0)

        return (int(sphere["color"][0]*light),int(sphere["color"][1]*light),int(sphere["color"][2]*light))
    
    return BACKGROUND    


def distance(sphere,point):
    vec=sphere["center"]-point 
    return numpy.linalg.norm(vec)-sphere["radius"]




# Set up the window.
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),0, 32)
pygame.display.set_caption('Raytracing')
scene = pygame.PixelArray(windowSurface)

for i in range(WINDOWWIDTH):
    for j in range(WINDOWHEIGHT):
        
        scene[i,j]=rayTracing(i,j) 

while True:
    # Check for events.
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    pygame.display.update()