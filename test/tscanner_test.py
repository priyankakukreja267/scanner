import sys
sys.path.append("/home/priyanka/15618/scanner")
from src.tscanner import TScanner
from kernels.histogram import HistogramKernel
from glob import glob

tscanner = TScanner("/home/priyanka/15618/scanner/examples/some_dir/")
#tscanner.ingest(glob("../data/gc-a*.mkv"))
tscanner.ingest(["./examples/vid.mp4"])
tscanner.declare_inputs(["def_col"])
tscanner.task(["def_col"], HistogramKernel(), ["histogram"])
tscanner.declare_output("histogram")
tscanner.run()
