import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import re

#Read in the file containing vertices into a 2D list
vertices = []
infile = open('face-vertices.data', 'r')
for line in infile:
    vertices.append([float(i) for i in line.split(',')])
infile.close()

#Read in the file containing indices to the vertices into a 2D list
indices = []
infile = open('face-index.txt', 'r')
for line in infile:
    if line != '\n':
        indices.append([int(i) for i in line.split(',')])
infile.close()

#Takes in the lists of vertices and indices, the user's choice of coordinate or wire frame display, and the distance of the eye with respect to the image
def plot(vertices, indices, ans, d):
    xa = []
    ya = []
    i = 0
    for index in indices:
        i += 1
        for point in index:
            #Take in the vertices of a triangle and use perspective projection to put the triangles in an XY plot
            x = vertices[point][0]
            y = vertices[point][1]
            z = vertices[point][2]
            xa.append(proj(x, z, d))
            ya.append(proj(y, z, d))
        if (ans == 2): #For wire frame
            #These first elements are appended at the end so that the third and final edge of a triangle is drawn
            xa.append(xa[0])
            ya.append(ya[0])
            plt.plot(xa, ya, markersize = 1, color = "blue", linewidth = 0.5)
            #Reset the lists to contain the next set of vertices
            xa *= 0
            ya *= 0 

    if (ans == 1): #For coordinate display
        plt.scatter(xa, ya, 1)

def proj(a, z, d): #This converts an x or y value of a 3D coordinate into a 2D one through the formula of perspective projection
    return a/(1 + z/d)

while True:
    try:
        ans = int(input("Press 1 for point display or 2 for wireframe display: "))
        d = float(input("Input a distance d: "))
        break
    except ValueError:
        print("Please input either 1 or 2, and a number for the distance.\n")

plot(vertices, indices, int(ans), float(d))
plt.show()
