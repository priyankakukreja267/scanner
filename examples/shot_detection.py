import Kernel
import TScanner
import Kernel_Registry

def func_name(vTable1):
	vTable2 = do_processing(vTable1)
	return vTable2


# Illustrate the end-to-end execution of how to detect shots in a video
tscanner = Tscanner()

# creates 1 table per video each table has a column named index, a column named image_data
vTable1 = tscanner.ingest([“video1”]) 

# Registry contains predefined kernels. Can add more to it.
reg = Kernel_Registry()
reg.initialize_kernel_registry()

# kernel for brightness
kernel1 = reg.lookup_registry('brightness')
if kernel1 is None:
	kernel1 = reg.register_new_kernel('myBrightness', func_name)

# kernel for edge_detection
kernel2 = reg.lookup_registry('edge_detection')
if kernel2 is None:
	kernel2 = reg.register_new_kernel('myEdgeDetection', func_name)

# This required kernel to take 2 inputs and return 2 outputs
db = Database()
vTable2 = db.new_table()
tscanner.task(vTable1, kernel1, vTable2)
vTable3 = db.new_table()
tscanner.task(vTable2, kernel2, vTable3)

# Select the column to be flushed to memory
tscanner.declare_ouput(vTable2.col3)
tscanner.declare_ouput(vTable3.col3)

# Run the pipeline
tscanner.run()
