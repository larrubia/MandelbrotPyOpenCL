'''
Classic Mandelbrot Set Algorithm using Threading
DEVICE INFO: Macbook PRO 16GB 2,6 GHz 6-Core Intel Core i7
macOS: Ventura
@author Alessandra Larrubia
'''

import threading
from PIL import Image
import matplotlib.pyplot as plt
from timeit import default_timer as timer

# Fractals are infinitely repeating patterns on different scales

xSize = ySize = 2048 # defines a finite number of pixels on axes x and y.
image = Image.new("RGB", (xSize, ySize))
imageSize = xSize * ySize
maxIt = 256 # defines the maximun number of interactions allowed
# drawing region (xa < xb & ya < yb): defined the domain plan
xa = -2.0 # defines the begin of the real axis X: from xa
xb = 0.5 # defines the end of the real axis X: to xb
ya = -1.25 # defines the begin of the imaginary axis Y: from ya
yb = 1.25 # defines the end of the imaginary axis Y: to yb

xd = xb - xa # defines x dimension
yd = yb - ya # defines y dimension

numThr = 2 # number of threads to run

class MandelbrotThread(threading.Thread):
    
    print ()
    print ('---------------------------------------------------------------------------------------------------------------------------------------------------------')
    print ('ALGORITHM INFO')
    print ()
    print('Generating fractal image of size {0} x {1} with {2} interactions using {3} threads'.format(xSize, ySize, maxIt, numThr)) 

    def __init__ (self, k):
          self.k = k
          threading.Thread.__init__(self)
          #print("Executing thread ", k)

    def run(self):
        # each thread only calculates its own share of pixels on the domain plan
        for i in range(t, imageSize, numThr):
            kx = i % xSize #calculates module to define pixels width
            ky = int(i / xSize) #calculates module to define pixels height
            xvalue = xa + xd * kx / (xSize - 1.0) # for every row: associates values to the axis x
            yvalue = ya + yd * ky / (ySize - 1.0) # for every col: associates values to the axis Y
            nReal = xvalue
            nImag = yvalue
            for n in range(maxIt):
                nReal2 = nReal * nReal
                nImag2 = nImag * nImag
                nImag = 2.0 * nReal * nImag + yvalue 
                nReal = nReal2 - nImag2 + xvalue                
                if nReal2 + nImag2 > 4:                    
                    # various color palettes can be created here
                    red = (n % 8) * 32
                    green = (20 - n % 20) * 20
                    blue = (n % 15) * 15
                    image.putpixel((kx, ky), (red, green, blue))

                    break

if __name__ == "__main__":
    tArr = []
    for t in range(numThr): # create all threads
        tArr.append(MandelbrotThread(t))

    start = timer()
    for t in range(numThr): # start all threads
        tArr[t].start()
    
    
    for t in range(numThr): # wait until all threads finished
        tArr[t].join()

    duration = timer() - start
    print(f'Total processing time: {duration:.2f} seconds')    
    print ()
    print ('---------------------------------------------------------------------------------------------------------------------------------------------------------')
    image.show()