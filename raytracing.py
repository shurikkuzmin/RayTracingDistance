import pygame
import sys
from pygame.locals import *
import numpy
import perlin
from scipy.interpolate import Rbf
WINDOWHEIGHT=300
WINDOWWIDTH=300
W=1.0
H=1.0
L=1.0

pygame.init()
RED=(255,0,0)
BACKGROUND=(255,255,255)
BLACK=(0,0,0)
ORANGE=(255,165,0)
BLUE=(0,0,255)

eye=numpy.array([0.0,0.0,0.0])
sphere={}
sphere["radius"]=1
sphere["center"]=numpy.array([0.0,0.0,3.0])
sphere["color"]=RED

lightSource={}
lightSource["center"]=numpy.array([1.5,1.5,1.0])

# Set up the Perlin's noise
NPERLIN = 31
x = numpy.linspace(0.0,10.0-10.0/(NPERLIN-1),NPERLIN)
y = numpy.linspace(0.0,10.0-10.0/(NPERLIN-1),NPERLIN)

res = numpy.zeros((NPERLIN,NPERLIN))
for i, xCoor in enumerate(x):
    for j, yCoor in enumerate(y):
        res[i,j] = perlin.noise(xCoor,yCoor)
phi = 2*numpy.pi/10.0 * x
theta = numpy.pi/10.0 * y
phiMesh,thetaMesh = numpy.meshgrid(phi,theta)
rbf = Rbf(phiMesh,thetaMesh,res)

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
    isSphereTouched = False
    isSphereTouched2 = False

    for iteration in range(50):
        dist=distance(sphere,point,isSphereTouched)
        if dist<0.0:
            isTouched=True 
            break
        dist=max(0.0001,dist)
        point=point+dist*vecE
    if isTouched:
        vecLight=lightSource["center"]-point
        vecLight=vecLight/numpy.linalg.norm(vecLight)
        #vecSphere=point-sphere["center"]
        #vecSphere=vecSphere/numpy.linalg.norm(vecSphere)
        vecSurface=numpy.array([0.0,0.0,0.0])
        eps = 0.001
        dist = distance(sphere,point, isSphereTouched)
        vecSurface[0] = distance(sphere,point+numpy.array([eps,0.0,0.0]),isSphereTouched2)-dist
        vecSurface[1] = distance(sphere,point+numpy.array([0.0,eps,0.0]),isSphereTouched2)-dist
        vecSurface[2] = distance(sphere,point+numpy.array([0.0,0.0,eps]),isSphereTouched2)-dist
        vecSurface = vecSurface/numpy.linalg.norm(vecSurface)

        cosA=vecLight[0]*vecSurface[0]+vecLight[1]*vecSurface[1]+vecLight[2]*vecSurface[2]
        light=0.2
        if cosA>0.0:
            light=min(light+cosA,1.0)
        twoPi=2*numpy.pi 
        #light=light*abs(vecSphere[0]+vecSphere[1]+vecSphere[2])/3.0
        #light=light*abs(numpy.cos(2*vecSphere[0]*twoPi)*numpy.cos(2*vecSphere[1]*twoPi)*numpy.cos(2*vecSphere[2]*twoPi))
        if not isSphereTouched:
            if (int((point[0]-100.0)/0.3)+int(point[2]/0.3))%2==0:
                color=BLACK
            else:
                color=BLUE
        else:    
            dist=numpy.linalg.norm(point-sphere["center"])
            color=BACKGROUND
            if dist>0.85 and dist<1.0:
                color=ORANGE
            elif dist>=1.0 and dist<1.1:
                color=RED
            elif dist>=1.1:
                color=BLACK

         

        return (int(color[0]*light),int(color[1]*light),int(color[2]*light))
    
    return BACKGROUND    


def distance(sphere,point,isSphereTouched):
    vec=sphere["center"]-point
    #vec2=point-sphere["center"]
    #vec2=vec2/numpy.linalg.norm(vec2)
    #twoPi=2*numpy.pi 
    #pheta = numpy.pi+numpy.arctan2(vec2[0],vec2[1])
    #theta = numpy.arctan2(vec2[2],numpy.sqrt(vec2[0]**2+vec2[1]**2))
    #valueNoise = rbf(pheta,theta)
    #phetaIndex = int((numpy.pi+numpy.arctan2(vec2[0],vec2[1]))/(twoPi)*(NPERLIN-1))
    #thetaIndex = int(numpy.arctan2(vec2[2],numpy.sqrt(vec2[0]**2+vec2[1]**2))/numpy.pi*(NPERLIN-1))
    dist1 = numpy.linalg.norm(vec)-sphere["radius"]
    dist2 = point[1]+1.0
    if dist1 > dist2:
        isSphereTouched = True
        return dist1
    isSphereTouched = False
    return dist2
    #numpy.linalg.norm(vec)-(sphere["radius"]+0.3*numpy.cos(2.0*vec2[0]*twoPi)*numpy.cos(2.0*vec2[1]*twoPi)*numpy.cos(2.0*vec2[2]*twoPi)))
    #return numpy.linalg.norm(vec)-(sphere["radius"]+3*valueNoise)

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