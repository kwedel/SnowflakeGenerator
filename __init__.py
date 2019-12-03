import numpy as np
import matplotlib.pyplot as plt
import svgwrite

from numpy.random import random

class snowflake:
    '''A class to generate snowflakes using Diffusion
    Limited Aggregation (DLA).
    '''
    def __init__(self,domain_size=20, crystal_size=1, step_size=0.1, angle=np.pi/12):
        self.domain_size = domain_size
        self.crystal_size = crystal_size
        self.c_size_sq = crystal_size**2
        self.crystals = [np.array([0,0])]
        self.step_size = step_size
        self.angle = angle
        self.bonds = []
        self.paths = []
    
    def add_crystal(self,):
        coords = np.array([self.domain_size, random()*self.domain_size * np.tan(np.pi/6)])
        self.paths.append([])
        collision = False
        while not collision:
            self.paths[len(self.crystals) - 1].append(coords)
            # Take a step
            coords = self._step(coords)
            # Check bounds
            if coords[1] < 0:
                coords[1] *= -1
            if coords[1] > np.tan(np.pi / 6) * coords[0]:
                coords = self._mirror_in_line(coords)
            # Check dists
            for i,c in enumerate(self.crystals):
                if self._dist_sq(c,coords) < self.c_size_sq:
                    collision = True
                    self.crystals.append(coords)
                    self.bonds.append((i,len(self.crystals)-1))
                    break
                    
    def export(self,filename='snowflake.svg',N=60,size=5,crystal_scale=1,style='circles'):
        '''size in cm'''
        svg = svgwrite.Drawing(filename=filename, size=('5cm','5cm'))
        scale = 37.795*size/(2*self.domain_size)
        translate = [scale*self.domain_size,scale*self.domain_size]
        circs = np.array(self.crystals[:N])
        circs = np.concatenate((circs, circs*[1,-1]))
        circs = np.concatenate((circs, circs*[-1,1]))
        theta = np.radians(60)
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c,-s), (s, c)))
        rotcircs = circs @ R
        circs = np.concatenate((circs,
                                rotcircs, rotcircs*[1,-1]))
        circs = scale * circs + translate
        for c in circs:
            svg.add(svg.circle(c, r=scale/2 * crystal_scale))
        self.svg = svg
        svg.save()
        
                
    def _dist_sq(self,p1,p2):
        return np.sum((p1-p2)**2)
                
    def _mirror_in_line(self,p, a=np.tan(np.pi/6), b=0):
        '''Mirror a point, p, in a line, l=(a,b), with format y = ax + b.'''
        x1,y1 = p
        # Perpendicular line y = -a**-1 + d
        d = y1 + a**(-1) * x1
        # Intersection
        x_int = (b - d)/(-a**(-1) - a)
        x2 = 2 * x_int - x1
        y2 = -a**(-1) * x2 + d
        return np.array([x2,y2])
            
    def _step(self,coords):
        theta = np.pi * random() + np.pi/2 + self.angle
        step = self.step_size * np.array([np.cos(theta), np.sin(theta)])
        return coords + step
