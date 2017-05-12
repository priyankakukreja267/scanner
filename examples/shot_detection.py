import os
import sys
matt = "MATT" in os.environ
if not matt:
    sys.path.append("/home/priyanka/15618/scanner")
from src.tscanner import TScanner
from kernels.histogram import HistogramKernel
import time
import pickle
from scipy.spatial import distance
import cv2
import numpy as np


WINDOW_SIZE = 500

def compute_shot_boundaries(hists):
    # Compute the mean difference between each pair of adjacent frames
    diffs = np.array([np.mean([distance.chebyshev(hists[i-1][j], hists[i][j]) for j in range(3)]) for i in range(1, len(hists))])
    diffs = np.insert(diffs, 0, 0)
    n = len(diffs)

    # Do simple outlier detection to find boundaries between shots
    boundaries = []
    for i in range(1, n):
        window = diffs[max(i-WINDOW_SIZE,0):min(i+WINDOW_SIZE,n)]
        if diffs[i] - np.mean(window) > 3 * np.std(window):
            boundaries.append(i)
    return boundaries


def make_montage(n, frames):
    _, frame = frames.next()
    frame = frame[0]
    (frame_h, frame_w, _) = frame.shape
    target_w = 64
    target_h = int(target_w / float(frame_w) * frame_h)
    frames_per_row = 16
    img_w = frames_per_row * target_w
    img_h = int(math.ceil(float(n) / frames_per_row)) * target_h
    img = np.zeros((img_h, img_w, 3))

    def place_image(i, fr):
        fr = cv2.resize(fr, (target_w, target_h))
        fr = cv2.cvtColor(fr, cv2.COLOR_RGB2BGR)
        row = i / frames_per_row
        col = i % frames_per_row
        img[(row * target_h):((row+1) * target_h),
            (col * target_w):((col+1) * target_w),
            :] = fr

    place_image(0, frame)
    for i, (_, frame) in enumerate(frames):
        place_image(i + 1, frame[0])

    return img


def load_frames(movie_path, boundaries):
    vid = cv2.VideoCapture(movie_path)


    return frames


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
    tscanner.run(n_threads=128)
    print('\nTime: {:.1f}s'.format(time.time() - s))


    s = time.time()
    print('Computing shot boundaries...')
    # Read histograms from disk
    f = open('/home/priyanka/15618/scanner/examples/some_dir/0_histogram.dat', 'rb')
    hists = []
    while True:
        try:
            hists.extend(pickle.load(f))
        except EOFError:
            break
    f.close()
    n = 256
    hists = [[h[i:i + n] for i in range(0, len(h), n)] for h in hists]
    boundaries = compute_shot_boundaries(hists)
    print('Time: {:.1f}s'.format(time.time() - s))


    print('Creating shot montage...')
    
    print('')

    print('Successfully generated shots.jpg')

    # tscanner.declare_output("??")


if __name__ == "__main__":
    main()
