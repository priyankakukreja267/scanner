from src import database
from PIL import Image
from glob import glob

db = database.Database('db_dir')
#db.add_column(database.ColumnSpecification("some_data", dtype='float'))
print(db.schema.columns)

db.ingest(["../data/kite.mkv"] + glob("../data/gc-a1.mkv"))
frame_reader = db.reader(["def_col"])
dat_writer = db.writer(["some_data"])

i_frame = 0
for frame in frame_reader:
    i_frame +=1
    if i_frame % 100 == 0:
        print("Loaded frame {}".format(i_frame))
    if i_frame % 1000 == 0:
        i = Image.fromarray(frame[0])
        i.save("frames/frame_{}.png".format(i_frame))
