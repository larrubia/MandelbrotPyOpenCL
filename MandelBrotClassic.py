'''
Classic Sequential Mandelbrot Set Algorithm
DEVICE INFO: Macbook PRO 16GB 2,6 GHz 6-Core Intel Core i7
macOS: Ventura
@author Alessandra Larrubia
'''

import numpy as np
from timeit import default_timer as timer
from PIL import Image
import matplotlib as mpl
import matplotlib.pyplot as plt

# Fractals are infinitely repeating patterns on different scales

# The function calculates whether or not the point of x and Y passed as parameters belongs to the Mandelbrot set
def mandelbrotset(xvalue, yvalue, maxiter): 
    nReal = xvalue # saves the xvalue parameter passed 
    nImag = yvalue # saves the yvalue parameter passed 
    for n in range(maxiter):
        nReal2 = nReal * nReal
        Nimag2 = nImag * nImag
        nImag = 2 * nReal * nImag + yvalue
        nReal = nReal2 - Nimag2 + xvalue
        if nReal2 + Nimag2 > 4.0:
            break
    return n # returns the number of iterations necessary to determine the pertinence of the values for Mandelbrot set

if __name__ == '__main__': # allows to execute code when the file runs as a script, but not when it’s imported as a module
    # defines the size of the axes X and Y: real and imaginary axes (complex numbers)
    xSize = ySize = 2048 #defines a finite number of pixels on axes x and y.
    x0 = -2.00 # defines the begin of the real axis X: from x0
    y0 = -1.25 # defines the begin of the imaginary axis Y: from y0
    x1 = 0.50 # defines the end of the real axis X: to x1
    y1 = 1.25 # defines the end of the imaginary axis Y: to y1

    maxIterations = 256 # defines the maximun number of interactions

    pixelWidth = (x1-x0) / xSize # defines each pixel width
    pixelHeight = (y1-y0) / ySize # defines each pixel height

    print ()
    print ('---------------------------------------------------------------------------------------------------------------------------------------------------------')
    print ('ALGORITHM INFO')
    print ()
    print('Generating fractal image of size {0} x {1} with {2} interactions'.format(xSize, ySize, maxIterations))
    
    start = timer() # saves the processing start time
    
    img = np.zeros((xSize, ySize), dtype = np.int32) # defines the domain plan
    for j in range(ySize): # for every col: associates values to theb axis Y (cy) 
        cy = y0 + j*pixelHeight
        for i in range(xSize): # for every row: associates values to the axis X (cx)
            cx = x0 + i * pixelWidth
            mandelbrotExec = mandelbrotset(cx, cy, maxIterations) # assign the function mandelbrotset, pass the attributes and execute it
            img[j, i] = mandelbrotExec # creates the domain plan through the result returned by the function mandelbrotset and keeped in mandelbrotExec

    duration = timer() - start # calculates the whole processing time
    print(f'Execution time: {duration:.2f} seconds')
    print ()
    print ('---------------------------------------------------------------------------------------------------------------------------------------------------------')
    plt.axis("off") # disables the display of the number line of the axes
    plt.imshow(img, plt.cm.get_cmap('twilight_shifted')) # plots the mandelbrot figure through the colorset indicated
    plt.show() # displays the mandelbrot figure

