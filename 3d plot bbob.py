# -*- coding: utf-8 -*-
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import numpy as np

import bbobbenchmarks

#########User-configured Parameters:
#Numbered from 1 (Sphere Function) to 24 (Lunacek bi-Rastrigin Function)
#as they occur in http://coco.lri.fr/downloads/download15.03/bbobdocfunctions.pdf
ProblemID=8

#Range for X,Y to display
xLimitLower = -5.01
xLimitUpper = 5.01
yLimitLower = -5.01
yLimitUpper = 5.01

#Samplepoints per dimension (remember the total number of points is samplepoints²)
samplepoints = 101

#Range below/above the optimal function value - keep in mind this is minimization!
zLimitBelow = 10 # "empty" space below opt f-value
zLimitAbove = 100 # added range which is shown of the function above the opt f-value
#If you don't care and want automatically determined values for the given X/Y-rectangle
autoZ = True

#########SCRIPT#########
problem, optimalFunValue = bbobbenchmarks.instantiate(ProblemID,1)
#one eval is needed so xopt exists
problem._evalfull(np.array([0,0]))
print('Problem: ' + str(ProblemID))
print('Optimal Solution Vector: ' + str(problem.xopt))
print('Optimal Function Value: ' + str(optimalFunValue))

@np.vectorize
def func(x, y):
    coord = np.array([x-xopt,y-yopt])
    _, funValue = problem._evalfull(coord)
    return funValue

#Generating the global optimum somewhere inside [-4,4]
xopt = np.random.uniform(-4,4)
yopt = np.random.uniform(-4,4)

fig = plt.figure()
ax = fig.gca(projection='3d')

#Defining the grid of probing points, and how many of them
X = np.linspace(-5, 5, samplepoints)
Y = np.linspace(-5, 5, samplepoints)
Z = func(X[:,None], Y[None,:])

X, Y = np.meshgrid(X, Y) #needed for getting everything plotted

#Plot itself
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=True)

#Defining the "Viewport"
ax.set_xlim(-5.01,5.01)
ax.set_ylim(-5.01,5.01)
if(autoZ):
    print('automatic z-limits by matplotlib')
else:
    ax.set_zlim(optimalFunValue - zLimitBelow, optimalFunValue + zLimitAbove)

#Inverting the zaxis makes for better images
plt.gca().invert_zaxis()

plt.show()

#For future use, changes format of the axis labeling
#x.zaxis.set_major_locator(LinearLocator(10))
#ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

#If one wants to see the colorbar
#fig.colorbar(surf, shrink=0.5, aspect=5)