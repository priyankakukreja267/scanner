import Kernel
import TScanner
from .util.unique_id_dict import UniqueIDDict
from Custom_kernel import custom_kernel

def func_name(vTable1):
	vTable2 = do_processing(vTable1)
	return vTable2

# Illustrate the end-to-end execution of how to detect shots in a video
tscanner = Tscanner()

# creates 1 table per video each table has a column named index, a column named image_data
vTable1 = tscanner.ingest([“video1”]) 

# kernel for brightness
kBrightness = Brightness()

# kernel for edge_detection
kCustom = Custom_kernel()

# This required kernel to take 2 inputs and return 2 outputs
db = Database()

tscanner.task('frames', kBrightness, 'col2')
tscanner.task('col2', kCustom, 'col3')

# Select the column to be flushed to memory
tscanner.declare_ouput('col3')
tscanner.declare_ouput('col2')

# Run the pipeline
tscanner.run()
