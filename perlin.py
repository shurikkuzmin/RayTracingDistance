import pylab
import numpy
import random

NX = 11
NY = 11

grad = numpy.zeros((NX,NY,2))

for i in range(NX):
    for j in range(NY):
        grad[i,j,0] = random.random()
        grad[i,j,1] = random.random()
        norm = numpy.sqrt(grad[i,j,0]**2 + grad[i,j,1]**2)
        grad[i,j,0] = grad[i,j,0]/norm
        grad[i,j,1] = grad[i,j,1]/norm

def interpolate(a0, a1, weight):
    return (1.0 - weight)*a0 + weight * a1

def gradient(iX,iY,x,y):
    deltaX = x - iX
    deltaY = y - iY

    return deltaX * grad[iX,iY,0] + deltaY * grad[iX,iY,1]

def perlin(x, y):
    x0 = int(x)
    x1 = x0 + 1
    y0 = int(y)
    y1 = y0 + 1
    deltaX = x - x0
    deltaY = y - y0

    corner1 = gradient(x0, y0, x, y)
    corner2 = gradient(x1, y0, x, y)
    interp12 = interpolate(corner1, corner2, deltaX)

    corner3 = gradient(x0, y1, x, y)
    corner4 = gradient(x1, y1, x, y)
    interp34 = interpolate(corner3, corner4, deltaX)
    return interpolate(interp12, interp34, deltaY)

x = numpy.linspace(0.0,10.0-10.0/30,31)
y = numpy.linspace(0.0,10.0-10.0/30,31)
X,Y = numpy.meshgrid(x,y)

res = numpy.zeros_like(X)
for i, xCoor in enumerate(x):
    for j, yCoor in enumerate(y):
        res[i,j] = perlin(xCoor,yCoor)
pylab.imshow(res)
pylab.show()