import sys
sys.path.append("/home/priyanka/15618/scanner")
from glob import glob
from src import kernel
from src import tscanner
from src import edge_detector
from src import gaussian_blur
from src import brightness


def func_name(vTable1):
	vTable2 = do_processing(vTable1)
	return vTable2


# Illustrate the end-to-end execution of how to detect shots in a video
# some_dir: directory in which to store any additional database data
myscanner = tscanner.TScanner('/home/priyanka/15618/scanner/examples/some_dir/')

# creates 1 table per video each table has a column named index, a column named image_data
myscanner.ingest(['./examples/vid.mp4'])

# kernel for gaussian blur
kBlur = gaussian_blur.Gaussian_Blur(5)

# kernel for brightness
kBrightness = brightness.Brightness(10)

# kernel for edge_detection
kEdgeDetector = edge_detector.Edge_Detector()

myscanner.declare_inputs(["def_col"])

# Define the operations in the pipeline
# myscanner.task(['frames'], kBrightness, ['col2'])
myscanner.task(['def_col'], kEdgeDetector, ['hor_edges'])

# Select the column to be flushed to memory
myscanner.declare_output('hor_edges')

# Run the pipeline
myscanner.run()
