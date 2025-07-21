import pygame as pg
import numpy as np
import time
from numpy import fft

def gauss(x, mu, sigma) : 
    return np.exp(-0.5*((x-mu)/sigma)**2)
def gauss1(x,mu,sigma, coef):
    return np.where(x >= 1,0,coef*np.exp(-0.5*((x-mu)/sigma)**2))  
def gauss2(x,mu,sigma, coef):
    return np.where(x >= 2,0,np.where(x<1,0,coef*np.exp(-0.5*((x%1-mu)/sigma)**2)))
def gauss3(x,mu,sigma, coef):
    return np.where(x >= 3,0,np.where(x<2,0,coef*np.exp(-0.5*((x%1-mu)/sigma)**2)))

class Grille:
    def __init__(self, N: int, M: int, radius: int, mu=0.5, sigma=0.15):
        y, x = np.ogrid[-N // 2: N // 2, -M // 2: M // 2]
        #On fait plusieurs convolutions
        distance1 = np.sqrt((x) ** 2 + (y) ** 2) / radius * 3  # 3 anneaux
        distance2 = np.sqrt((x) ** 2 + (y) ** 2) / radius * 2  # 2 anneaux
        distance3 = np.sqrt((x) ** 2 + (y) ** 2) / radius   # 1 anneau
        self.kernels = []
        self.kernels_fft = []

        # Première convolution (3 anneau)
        kernel1 = gauss1(distance1, mu, sigma,1) + gauss2(distance1, mu, sigma,5/12) + gauss3(distance1, mu, sigma,2/3)
        kernel1 /= np.sum(kernel1)
        self.kernels.append(kernel1)
        self.kernels_fft.append(fft.fft2(np.fft.fftshift(kernel1)))

        # Deuxième convolution (2 anneau)
        kernel2 = gauss1(distance2, mu, sigma, 1 / 12) + gauss2(distance2, mu, sigma,1)
        kernel2 /= np.sum(kernel2)
        self.kernels.append(kernel2)
        self.kernels_fft.append(fft.fft2(np.fft.fftshift(kernel2)))

        # Troisième convolution (1 anneau)
        kernel3 = gauss1(distance3, mu, sigma,1)
        kernel3 /= np.sum(kernel3)
        self.kernels.append(kernel3)
        self.kernels_fft.append(fft.fft2(np.fft.fftshift(kernel3)))

    def accroissement(self, x, mu, sigma):
    	return -1 + 2 * gauss(x,mu, sigma)

    def compute_next_iteration(self, cells, dt=0.1):
	#On a donc 3 energies a traité
        energy1 = np.real(fft.ifft2(self.kernels_fft[0]*fft.fft2(cells))) 
        energy2 = np.real(fft.ifft2(self.kernels_fft[1]*fft.fft2(cells))) 
        energy3 = np.real(fft.ifft2(self.kernels_fft[2]*fft.fft2(cells)))              
        acc = np.mean([self.accroissement(energy1,0.156,0.0118) ,self.accroissement(energy2,0.193,0.049) ,self.accroissement(energy3,0.342,0.0891)], axis=0)
        cells = np.clip(cells + dt *acc, 0, 1)
        return cells

# Classe Drawing
class Drawing:
    def __init__(self, width=800, height=600):
        self.colors = np.array([np.ogrid[0.:255.:256j], np.ogrid[0.:255.:256j], np.ogrid[0.:255.:256j]]).T
        self.dimensions = (width, height)
        self.screen = pg.display.set_mode(self.dimensions)

    def draw(self, cells):
        indices = (255 * cells).astype(dtype=np.int32)
        surface = pg.surfarray.make_surface(self.colors[indices.T])
        surface = pg.transform.flip(surface, False, True)
        surface = pg.transform.scale(surface, self.dimensions)
        self.screen.blit(surface, (0, 0))
        pg.display.update()

# Initialisation
N = 128
M = int(np.ceil((16*N)/9))

fish = np.array([[0,0,0,0,0,0,0,0,0,0,0,0.06,0.1,0.04,0.02,0.01,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0.15,0.37,0.5,0.44,0.19,0.23,0.3,0.23,0.15,0.01,0,0,0,0], [0,0,0,0,0,0,0.32,0.78,0.26,0,0.11,0.11,0.1,0.08,0.18,0.16,0.17,0.24,0.09,0,0,0], [0,0,0,0,0.45,0.16,0,0,0,0,0,0.15,0.15,0.16,0.15,0.1,0.09,0.21,0.24,0.12,0,0], [0,0,0,0.1,0,0,0,0,0,0,0,0.17,0.39,0.43,0.34,0.25,0.15,0.16,0.15,0.25,0.03,0], [0,0.15,0.06,0,0,0,0,0,0,0,0.24,0.72,0.92,0.85,0.61,0.47,0.39,0.27,0.12,0.18,0.17,0], [0,0.08,0,0,0,0,0,0,0,0,1.0,1.0,1.0,1.0,0.73,0.6,0.56,0.31,0.12,0.15,0.24,0.01], [0,0.16,0,0,0,0,0,0,0,0.76,1.0,1.0,1.0,1.0,0.76,0.72,0.65,0.39,0.1,0.17,0.24,0.05], [0,0.05,0,0,0,0,0,0,0.21,0.83,1.0,1.0,1.0,1.0,0.86,0.85,0.76,0.36,0.17,0.13,0.21,0.07], [0,0.05,0,0,0.02,0,0,0,0.4,0.91,1.0,1.0,1.0,1.0,1.0,0.95,0.79,0.36,0.21,0.09,0.18,0.04], [0.06,0.08,0,0.18,0.21,0.1,0.03,0.38,0.92,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.64,0.31,0.12,0.07,0.25,0], [0.05,0.12,0.27,0.4,0.34,0.42,0.93,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.97,0.33,0.16,0.05,0.1,0.26,0], [0,0.25,0.21,0.39,0.99,1.0,1.0,1.0,1.0,1.0,1.0,0.86,0.89,0.94,0.83,0.13,0,0,0.04,0.21,0.18,0], [0,0.06,0.29,0.63,0.84,0.97,1.0,1.0,1.0,0.96,0.46,0.33,0.36,0,0,0,0,0,0.03,0.35,0,0], [0,0,0.13,0.22,0.59,0.85,0.99,1.0,0.98,0.25,0,0,0,0,0,0,0,0,0.34,0.14,0,0], [0,0,0,0,0.33,0.7,0.95,0.8,0.33,0.11,0,0,0,0,0,0,0,0.11,0.26,0,0,0], [0,0,0,0,0.16,0.56,0.52,0.51,0.4,0.18,0.01,0,0,0,0,0,0,0.42,0,0,0,0], [0,0,0,0,0.01,0,0.33,0.47,0.33,0.05,0,0,0,0,0,0,0.35,0,0,0,0,0], [0,0,0,0,0,0.26,0.32,0.13,0,0,0,0,0,0,0,0.34,0,0,0,0,0,0], [0,0,0,0,0,0.22,0.25,0.03,0,0,0,0,0,0,0.46,0,0,0,0,0,0,0], [0,0,0,0,0,0,0.09,0.2,0.22,0.23,0.23,0.22,0.3,0.3,0,0,0,0,0,0,0,0]])

cells = np.zeros((N,M))
pos_x, pos_y = 100, 100
cells[pos_x:pos_x + fish.shape[0], pos_y:pos_y + fish.shape[1]] = fish

r = 10
grid = Grille(N,M,r)

appli = Drawing()

pg.init()
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

