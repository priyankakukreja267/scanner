import sys, os
matt = "MATT" in os.environ
if not matt:
    sys.path.append("/home/priyanka/15618/scanner")
from src.tscanner import TScanner
from glob import glob
import time

from kernels.face_detector import FaceDetectorKernel
from kernels.draw_box import DrawBoxKernel

tscanner = TScanner("db_dir" if matt else "./examples/some_dir")
tscanner.clear_db()
tscanner.ingest(glob("../data/kite_short*.mkv") if matt else ["./examples/vid1.mp4"])
tscanner.declare_inputs(["def_col"])

tscanner.task(["def_col"], FaceDetectorKernel(), ["face_detected"])
tscanner.task(["def_col", "face_detected"], DrawBoxKernel(), ["boxed"])
tscanner.declare_output("boxed")

t0 = time.time()
#cProfile.run('tscanner.run(n_threads=1)')
tscanner.run(n_threads=4)
t1 = time.time()
print('time taken in tscanner.run() = %s' % (t1-t0))
