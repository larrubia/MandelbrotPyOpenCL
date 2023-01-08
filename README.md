# Hardware INFO
DEVICE INFO: Macbook PRO 16GB 2,6 GHz 6-Core Intel Core i7

GRAPHICS: AMD Radeon Pro 5300M 4 GB

macOS: Ventura

# Sequential Programming
Algorithm that runs sequential instructions through a single processor.

# Parallel Programming
Algorithm composed of a set of parts that can be solved concurrently. Each part is also constituted by a series of sequential instructions, but which can be executed simultaneously by several processors.

# Parallel Computing
Can be defined as the use simultaneous use of several computational resources in order to reduce the time needed to solve a particular problem. 
These computational resources may include a single computer with multiple processors,an arbitrary number of networked computers or even the combination of both.

# Why Parallel Programming?

Traditionally, parallel programming had as its initial motivation the resolution and simulation of
fundamental problems in science and engineering with scientific and economic importance, known as Grand Challenge Problems - GCPs.

Nowadays, applications require the processing of large volumes of information each faster time. Parallel programming can reduce the time required to solve complex and larger problems, taking advantage of underutilized computational resources locally.

# Tasks performed during the semester

- Parallelization of matrices multiplication, using a shared memory programming model, using threads / tasks - JAVA
- Parallelization of the generation of a Mandelbrot Fractal, using a shared memory programming model, based on a task pool - JAVA with ForkJoinPool and RecursiveAction
- Vectorization algorithm to generate a Mandelbrot Fractal using GPU processing - Python with PyOpenCL

# Provided Algorithms

- Classic Sequential Mandelbrot Set Algorithm in Python
- Classic Mandelbrot Set Algorithm using Threading in Python
- Mandelbrot Set Algorithm using GPU Processing with PyOpenCL in Python

# Critical Analysis
Taking into account professional interest in data science area, this analysis will focus only on algorithms that used the Python language.

Fractals are infinitely repeating patterns on different scales. Self-similarity can often be defined mathematically with recursion

The "Classic Sequential Mandelbrot Set Algorithm" was based on the sequential calculation of a recursive mathematical algorithm that generates a fractal image. Using this algorithm to generate a fractal image of size 2048 x 2048 with 256 interactions took 46.77 seconds.

![image](https://user-images.githubusercontent.com/62728284/211222690-4a15d35f-941d-4dcd-8e09-e55a75895c83.png)

In order to optimize the processing of the image generated through the classical sequential algorithm, a possible solution was sought in the use of threads for processing the calculation that originates the fractal image.

For this, the use of the threading module was investigated.
"The threading module contains a Thread class that we need to extend to create our own execution threads. The run method will contain the code we want to execute on the thread." (ORTEGA, 2020 - p.59)

Despite the existence of threading module, accordingly to McKinney, 2022, p.4 "Python can be a challenging language for building highly concurrent, multithreaded applications, particularly with many threads. The reason for this is that it has what is known as the Global Interpreter Lock (GIL), a mechanism that prevents the interpreter from executing more than one Python instruction at a time."

If Python doesn't allow algorithms to run in threads, how does it have a threading module?
The answer to this question is not as simple as it seems, as it involves an analysis of the types of problems to be solved when using the threading module in Python.

For the generation of the fractal figure, the use of the threading module did not even bring a higher performance in relation to the execution of the sequential code. This is probably because Python's implementation of threads doesn't run asynchronously. Adding threads multiplies the execution times in some cases. In "Classic Mandelbrot Set Algorithm using Threading in Python" the performance of the tasks didn´t improve the execution time once that only one thread can be executed at time , no matter how many processors the device have. 

Using the threading algorithm to generate a fractal image of size 2048 x 2048 with 256 interactions using 2 threads the total processing time was 49.22 seconds. Although dividing the processing in tasks it made the processing time to increase 2.45 seconds when compared to the sequential programm.

![image](https://user-images.githubusercontent.com/62728284/211222672-9277dba1-104d-4362-9985-f9114d752680.png)


It's important to note that using threads will not failure in all contexts. I also have used the same technique to collect data from an open data excel file and had a very interesting result. Unfortunately, for the scenario worked here, the result did not go as expected.

However, all is not lost in trying to optimize fractal imaging. There's still the option of using parallel processing through the GPU (Graphic Unit Processing).

For GPU parallel processing, Ii has been used PyOpenCL once the graphic unit was an AMD RADEON. For NVIDIA graphics devices it's possible to use PyCUDA.

"Andreas Klöckner of the Courant Institute of Mathematical Sciences has extended Python’s breadth of capabilities by releasing PyOpenCL." (SCARPINO, 2012, p.210)

PyOpenCL lets you access GPUs and other massively parallel computing devices from Python. Using a GPU can have hundreds of cores and thus optimize the algorithm. The focus is on the kernel, with numpy typing and it's necessary that the host application written in Python requires some code written in C. 

The use of PyOpenCL allowed to obtain the best performance of the algorithms used so far. Using GPU Processing with PyOpenCL algorithm to generate a fractal image of size 2048 x 2048 with 256 interactions took incredible 0.08 seconds! Processing was 500x faster.

![image](https://user-images.githubusercontent.com/62728284/211223128-5d251f8c-b9e7-4b88-a39e-a5a4f2ff8d57.png)

In short, using the GPU offers an excellent architecture for parallel operations that can be used to compute complex calculations.
