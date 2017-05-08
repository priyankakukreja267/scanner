import sys
sys.path.append("/home/priyanka/15618/scanner")
from src import kernel
from src import tscanner
from src import edge_detector

def func_name(vTable1):
	vTable2 = do_processing(vTable1)
	return vTable2


# Illustrate the end-to-end execution of how to detect shots in a video
# some_dir: directory in which to store any additional database data
myscanner = tscanner.TScanner('some_dir')

# creates 1 table per video each table has a column named index, a column named image_data
myscanner.ingest(['video1.mp4', 'video2.mp4'])

# kernel for gaussian blur
kBlur = Gaussian_Blur(5)

# kernel for brightness
kBrightness = Brightness(10)

# kernel for edge_detection
kEdgeDetector = Edge_Detector()

# Define the operations in the pipeline
# myscanner.task(['frames'], kBrightness, ['col2'])
myscanner.task(['frames'], kCustom, ['hor_edges', 'ver_edges'])

# Select the column to be flushed to memory
myscanner.declare_ouput('hor_edges')
myscanner.declare_ouput('ver_edges')

# Run the pipeline
myscanner.run()
