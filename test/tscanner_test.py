from tscanner import TScanner
from kernels.histogram import HistogramKernel
from glob import glob

tscanner = TScanner("db_dir")
#tscanner.ingest(glob("../data/gc-a*.mkv"))
tscanner.ingest(["../data/kite.mkv"])
tscanner.declare_inputs(["def_col"])
tscanner.task(["def_col"], HistogramKernel(), ["histogram"])
tscanner.declare_output("histogram")
tscanner.run()
