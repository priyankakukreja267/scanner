from src.tscanner import TScanner
from kernels.histogram import HistogramKernel
from kernels.gaussian_blur import GaussianBlur
from glob import glob

tscanner = TScanner("db_dir")
tscanner.clear_db()
#tscanner.ingest(glob("../data/gc-a*.mkv") + glob("../data/gc-b*.mkv"))
tscanner.ingest(["../data/kite.mkv"])
tscanner.declare_inputs(["def_col"])
blur_kernel = GaussianBlur()
tscanner.task(["def_col"], blur_kernel, ["histogram"])
tscanner.declare_output("histogram")
tscanner.run(n_threads=1)
