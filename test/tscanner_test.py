import sys
sys.path.append("/home/priyanka/15618/scanner")
from src.tscanner import TScanner
from kernels.histogram import HistogramKernel
from kernels.gaussian_blur import GaussianBlur
from glob import glob
import time

tscanner = TScanner("./examples/some_dir")
tscanner.clear_db()
tscanner.ingest(["./examples/vid1.mp4"])
tscanner.declare_inputs(["def_col"])
blur_kernel = GaussianBlur()
tscanner.task(["def_col"], blur_kernel, ["histogram"])
tscanner.declare_output("histogram")

t0 = time.time()
tscanner.run(n_threads=1)
t1 = time.time()
print('time taken in tscanner.run() = %s' % (t1-t0))
