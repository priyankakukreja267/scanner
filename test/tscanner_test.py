import sys, os
matt = "MATT" in os.environ
if not matt:
    sys.path.append("/home/priyanka/15618/scanner")
from src.tscanner import TScanner
from kernels.histogram import HistogramKernel
from kernels.gaussian_blur import Gaussian_Blur
from kernels.edge_detector import Edge_Detector
from glob import glob
import time
#import cProfile

tscanner = TScanner("db_dir" if matt else "./examples/some_dir")
tscanner.clear_db()
tscanner.ingest(glob("../data/kite_short*.mkv") if matt else ["./examples/clip.mp4"])
tscanner.declare_inputs(["def_col"])

blur_kernel = Gaussian_Blur(21)
ed_kernel = Edge_Detector()

tscanner.task(["def_col"], ed_kernel, ["edge_detected"])
tscanner.declare_output("edge_detected")
tscanner.task(["def_col"], blur_kernel, ["gaussian_blur"])
tscanner.declare_output("gaussian_blur")

t0 = time.time()
#cProfile.run('tscanner.run(n_threads=1)')
tscanner.run()
t1 = time.time()
print('time taken in tscanner.run() = %s' % (t1-t0))
