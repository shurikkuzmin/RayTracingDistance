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

eye=numpy.array([0.0,0.0,0.0])
sphere={}
sphere["radius"]=1
sphere["center"]=numpy.array([0.0,0.0,3.0])
sphere["color"]=RED

def convert(i,j):
    x= W/2-i/(WINDOWWIDTH-1)*W
    y= H/2-j/(WINDOWHEIGHT-1)*H
    z= L
    return numpy.array([x,y,z]) 

def rayTracing(i,j):
    screenPoint=convert(i,j)
    ray=screenPoint-eye   

# Set up the window.
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),0, 32)
pygame.display.set_caption('Raytracing')
scene = pygame.PixelArray(windowSurface)

#for i in range(WINDOWWIDTH):
#    for j in range(WINDOWHEIGHT):
#        
#        scene[i,j]=ray() 

while True:
    # Check for events.
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    pygame.display.update()