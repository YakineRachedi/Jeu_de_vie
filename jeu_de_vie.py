import pygame as pg
import numpy as np
from scipy.signal import convolve2d
from scipy.ndimage import gaussian_filter

def gauss(x, mu, sigma) : 
    return np.exp(-0.5*((x-mu)/sigma)**2)

class Grille:
    def __init__(self, radius : int, mu = 0.5, sigma = 0.15, color_life=pg.Color("black"), color_dead=pg.Color("white")):
    	#On crée un nouveau init qui a pour but d'adopter les anneaux, gauss etc
        y, x = np.ogrid[-radius: radius, -radius : radius]
        distance = np.sqrt((1+x)**2+(1+y)**2)/radius
        self.kernel = gauss(distance, mu, sigma)
        self.kernel[distance> 1] = 0 
        self.kernel /= np.sum(self.kernel) 
 
    def accroissement(self,x, mu = 0.15, sigma = 0.015) : 
    	return -1 + 2 * gauss(x,mu, sigma)

    def compute_next_iteration(self, cells, dt = 0.1):
    	energy = convolve2d(cells, self.kernel, mode='same', boundary='wrap')
    	acc = self.accroissement(energy)
    	cells = np.clip(cells + dt *acc, 0, 1)
    	return cells

class Drawing:
#Nouveau Drawing
    def __init__(self, width = 800, height = 600):
        self.colors = np.array([np.ogrid[0.:255.:256j], np.ogrid[0.:255.:256j], np.ogrid[0.:255.:256j]]).T
        self.dimensions = (width, height)
        self.screen = pg.display.set_mode(self.dimensions)

    def draw(self, cells):
        indices = (255*cells).astype(dtype=np.int32)
        surface = pg.surfarray.make_surface(self.colors[indices.T])
        surface = pg.transform.flip(surface, False, True)
        surface = pg.transform.scale(surface, self.dimensions)
        self.screen.blit(surface, (0,0))
        pg.display.update()

if __name__ == '__main__':
    import time
    import sys

    pg.init()
    
    #N = 512
    #M = int(np.ceil((16*N)/9))
    # Gaussian spot centered in the middle
    #radius = 36
    #y, x = np.ogrid[-N//2:N//2, -M//2:M//2]
    #cells = np.exp(-0.5 * (x*x + y*y) / (radius*radius))
    N = 256
    M = int(np.ceil((16*N)/9))

    orbium = np.array([[0,0,0,0,0,0,0.1,0.14,0.1,0,0,0.03,0.03,0,0,0.3,0,0,0,0], [0,0,0,0,0,0.08,0.24,0.3,0.3,0.18,0.14,0.15,0.16,0.15,0.09,0.2,0,0,0,0], [0,0,0,0,0,0.15,0.34,0.44,0.46,0.38,0.18,0.14,0.11,0.13,0.19,0.18,0.45,0,0,0], [0,0,0,0,0.06,0.13,0.39,0.5,0.5,0.37,0.06,0,0,0,0.02,0.16,0.68,0,0,0], [0,0,0,0.11,0.17,0.17,0.33,0.4,0.38,0.28,0.14,0,0,0,0,0,0.18,0.42,0,0], [0,0,0.09,0.18,0.13,0.06,0.08,0.26,0.32,0.32,0.27,0,0,0,0,0,0,0.82,0,0], [0.27,0,0.16,0.12,0,0,0,0.25,0.38,0.44,0.45,0.34,0,0,0,0,0,0.22,0.17,0], [0,0.07,0.2,0.02,0,0,0,0.31,0.48,0.57,0.6,0.57,0,0,0,0,0,0,0.49,0], [0,0.59,0.19,0,0,0,0,0.2,0.57,0.69,0.76,0.76,0.49,0,0,0,0,0,0.36,0], [0,0.58,0.19,0,0,0,0,0,0.67,0.83,0.9,0.92,0.87,0.12,0,0,0,0,0.22,0.07], [0,0,0.46,0,0,0,0,0,0.7,0.93,1,1,1,0.61,0,0,0,0,0.18,0.11], [0,0,0.82,0,0,0,0,0,0.47,1,1,0.98,1,0.96,0.27,0,0,0,0.19,0.1], [0,0,0.46,0,0,0,0,0,0.25,1,1,0.84,0.92,0.97,0.54,0.14,0.04,0.1,0.21,0.05], [0,0,0,0.4,0,0,0,0,0.09,0.8,1,0.82,0.8,0.85,0.63,0.31,0.18,0.19,0.2,0.01], [0,0,0,0.36,0.1,0,0,0,0.05,0.54,0.86,0.79,0.74,0.72,0.6,0.39,0.28,0.24,0.13,0], [0,0,0,0.01,0.3,0.07,0,0,0.08,0.36,0.64,0.7,0.64,0.6,0.51,0.39,0.29,0.19,0.04,0], [0,0,0,0,0.1,0.24,0.14,0.1,0.15,0.29,0.45,0.53,0.52,0.46,0.4,0.31,0.21,0.08,0,0], [0,0,0,0,0,0.08,0.21,0.21,0.22,0.29,0.36,0.39,0.37,0.33,0.26,0.18,0.09,0,0,0], [0,0,0,0,0,0,0.03,0.13,0.19,0.22,0.24,0.24,0.23,0.18,0.13,0.05,0,0,0,0], [0,0,0,0,0,0,0,0,0.02,0.06,0.08,0.09,0.07,0.05,0.01,0,0,0,0,0]])
    cells = np.zeros((N,M))
    pos_x = M//6
    pos_y = N//6
    cells[pos_x:(pos_x + orbium.shape[1]), pos_y:(pos_y + orbium.shape[0])] = orbium.T    
    grid = Grille( radius = 13)
    appli = Drawing()

    mustContinue = True
    while mustContinue:
        t1 = time.time()
        cells = grid.compute_next_iteration(cells = cells)
        t2 = time.time()
        appli.draw(cells)
        t3 = time.time()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                mustContinue = False
        print(f"Temps calcul prochaine generation : {t2 - t1:2.2e} secondes, temps affichage : {t3 - t2:2.2e} secondes\r", end='')
    pg.quit()
