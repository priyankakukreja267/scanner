from src import database
from PIL import Image
from glob import glob
import numpy as np

db = database.Database('db_dir')
db.add_column(database.ColumnSpecification("some_data", dtype='float'))
db.add_column(database.ColumnSpecification("garbage_data", dtype='uint32'))
db.add_column(database.ColumnSpecification("video_resized", video=True))

db.ingest(["../data/kite.mkv"] + glob("../data/gc-a1.mkv"))
frame_reader = db.reader(["def_col"])
dat_writer = db.writer(["some_data", "garbage_data"])

i_frame = 0
for changed_file, frame in frame_reader:
    i_frame +=1
    if changed_file:
        print("Changed file!")
        dat_writer.next_file()
    if i_frame % 100 == 0:
        print("Loaded frame {}".format(i_frame))
    if i_frame % 1000 == 0:
        i = Image.fromarray(frame[0])
        i.save("frames/frame_{}.png".format(i_frame))

    dat_writer.write_row([float(np.average(i_frame)), i_frame])
