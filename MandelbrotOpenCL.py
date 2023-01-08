'''
Mandelbrot Set Algorithm using GPU Processing with PyOpenCL
DEVICE INFO: Macbook PRO 16GB 2,6 GHz 6-Core Intel Core i7
GRAPHICS: AMD Radeon Pro 5300M 4GB
macOS: Ventura
@author Alessandra Larrubia
'''

import pyopencl as cl
import numpy as np
from PIL import Image
import matplotlib as mpl
import matplotlib.pyplot as plt
from timeit import default_timer as timer

width = 2048    #define a finite number of pixels on axis X
height = 2048   #define a finite number of pixels on axis Y
maxIt = 256    #define the maximun number of interactions allowed


#The kernel calculates in parallel if each value point on axis X if belongs to the complex plane.
#If it belongs to the complex plane, 0 is stored in buffer out (i.e the value belongs to the Mandelbrot set).

KernelSource = '''
__kernel void mandelbrot(const int width,
                         const int height,
                         const int maxIt,
                         __global int *out
                        )
{
    int x = get_global_id(0);
    int y = get_global_id(1);
    if (x >= width || y >= height) {
        return;
    }
    double nReal1 = x * 3.0 / (width - 1) - 2.0;  //for every row: associates values to the axis x
    double nImag1 = y * 3.0 / (height - 1) - 1.5; //for every col: associates values to the axis Y
    double nReal2 = 0.0;
    double nImag2 = 0.0;
    double tmp_x_real;
    double norm;
    int divergence_at = 0;

    for (int i = 1; i <= maxIt; ++i) {
        tmp_x_real = nReal2 * nReal2 - nImag2 * nImag2 + nReal1;
        nImag2 = 2 * nReal2 * nImag2 + nImag1;
        nReal2 = tmp_x_real;
        // if norm > 4.0, we can be sure that the sequence diverges
        norm = nReal2 * nReal2 + nImag2 * nImag2;
        if (norm > 4.0) {
            divergence_at = i;
            break;
        }
    }
    out[y * width + x] = divergence_at;
}
'''


def main():
    
    #Define open-cl queue and context
    platform = cl.get_platforms()[0] #Select the platform: Apple at 0x7fff0000
    device = platform.get_devices()[1] #Select the device on the previous platform: AMD Radeon Pro 5300M Compute Engine on 'Apple' at 0x1021e00>
    context =cl.Context([device]) #Create the context with the devices informed previously
    queue = cl.CommandQueue(context) #Create the queue to be used for processing using the selected device set up
    
    print ()
    print ('---------------------------------------------------------------------------------------------------------------------------------------------------------')
    print ('PROCESSING INFO')
    print ()
    print ('Generating fractal image of size {0} x {1} with {2} interactions using {3}'.format(width, height, maxIt, device)) 
       
    #Define the buffer on the device
    d_out = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, width * height * np.dtype(np.float64).itemsize)

    #Compile the KernelSource where the fractal will be calculated by the mandelbrot kernel
    program = cl.Program(context, KernelSource).build()
    mandelbrot = program.mandelbrot
    mandelbrot.set_scalar_arg_dtypes([np.int32, np.int32, np.int32, None])

    start = timer()

    #Run the Mandelbrot kernel cointained in KernelSource
    globalrange = (width, height)
    localrange = None
    mandelbrot(queue, globalrange, localrange, width, height, maxIt, d_out)
    queue.finish()

    #Copy the values stored in the buffer to the host-program.
    img = np.empty((height, width), dtype=np.int32) # create an array without initializing the entries of given shape and type
    cl.enqueue_copy(queue, img, d_out) 

    #Display the fractal image
    fractal = 255.0 * (img / np.max(img))
    duration = timer() - start
    print(f'Total processing time: {duration:.2f} seconds')  
    print ('---------------------------------------------------------------------------------------------------------------------------------------------------------')
    print ()  
    plt.axis("off") # disables the display of the number line of the axes
    plt.imshow(fractal, plt.cm.get_cmap('twilight_shifted')) # plots the mandelbrot figure through the colorset indicated
    plt.show() # displays the mandelbrot figure


if __name__ == "__main__":
    main()
