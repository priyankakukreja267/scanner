import os
import sys
sys.path.append("/home/priyanka/15618/scanner")
from src.tscanner import TScanner
from kernels.histogram import HistogramKernel
from glob import glob
import time

def main():
    movie_path = './examples/moana.mp4'
    print('Detecting shots in movie {}'.format(movie_path))
    movie_name = os.path.basename(movie_path)

    # device = DeviceType.CPU
    # scanner_montage = False

    print('Loading movie into Scanner database...')
    s = time.time()
    tscanner = TScanner("./examples/some_dir")
    tscanner.clear_db()
    tscanner.ingest([movie_path])
    tscanner.declare_inputs(["def_col"])
    print('Time: {:.1f}s'.format(time.time() - s))

        
    s = time.time()
    print('Computing a color histogram for each frame...')
    hist_kernel = HistogramKernel()
    tscanner.task(["def_col"], hist_kernel, ["histogram"])
    tscanner.declare_output("histogram")
    tscanner.run(n_threads=1)
    print('\nTime: {:.1f}s'.format(time.time() - s))



		# s = time.time()
        # print('Computing shot boundaries...')
        # # Read histograms from disk
        # hists = [h for _, h in hists_table.load(['histogram'],
        #                                         parsers.histograms)]
        # boundaries = compute_shot_boundaries(hists)
        # print('Time: {:.1f}s'.format(time.time() - s))

        # s = time.time()
        # print('Creating shot montage...')
        # if scanner_montage:
        #     # Make montage in scanner
        #     montage_img = make_montage_scanner(db, movie_table, boundaries)
        # else:
        #     # Make montage in python
        #     # Loading the frames for each shot boundary
        #     frames = movie_table.load(['frame'], rows=boundaries)
        #     montage_img = make_montage(len(boundaries), frames)

        # print('')
        # print('Time: {:.1f}s'.format(time.time() - s))

        # cv2.imwrite('shots.jpg', montage_img)
        # print('Successfully generated shots.jpg')

if __name__ == "__main__":
    main()
