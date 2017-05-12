import sys, os
matt = "MATT" in os.environ
if not matt:
    sys.path.append("/home/priyanka/15618/scanner")
from src.tscanner import TScanner
from kernels.histogram import HistogramKernel
from kernels.gaussian_blur import Gaussian_Blur
from glob import glob
import time
#import cProfile

tscanner = TScanner("db_dir" if matt else "./examples/some_dir")
tscanner.clear_db()
tscanner.ingest(glob("../data/kite_short*.mkv") if matt else ["./examples/moana.mp4"])
tscanner.declare_inputs(["def_col"])
blur_kernel = Gaussian_Blur(21)
tscanner.task(["def_col"], blur_kernel, ["gaussian_blur"])
tscanner.declare_output("gaussian_blur")

t0 = time.time()
#cProfile.run('tscanner.run(n_threads=1)')
tscanner.run(n_threads=2)
t1 = time.time()
print('time taken in tscanner.run() = %s' % (t1-t0))
