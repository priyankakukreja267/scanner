import sys, os
matt = "MATT" in os.environ
if not matt:
    sys.path.append("/home/priyanka/15618/scanner")
import time
import cv2
import numpy as np
import profilehooks



OUTPUT_FRAMERATE = 24
H264_FOURCC = cv2.VideoWriter_fourcc(*"h264")
face_cascade = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")


def face_detector(frame):
	grayscale = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
	faces = face_cascade.detectMultiScale(grayscale, 1.3, 5)
	coords = []
	for (x, y, w, h) in faces:
		coords.extend([x, y, w, h])
	return np.asarray(coords, dtype='int64')

def draw_boxes(frame, coords):
	for i in range(0, len(coords), 4):
		x, y, w, h = coords[i:i+4]
		frame = cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)
	return frame

def process_frame(frame):
	bounding_box = face_detector(frame)
	out_frame = draw_boxes(frame, bounding_box)
	return out_frame

@profilehooks.profile
def run_everything():
	# Read in the video
	# Detect faces
	# Draw bounding boxes
	# Output the video with bounding boxes drawn on it

	if matt:
		in_file = '../data/kite_short0.mkv'
		out_file = '../data/kite_short0_detected.mkv'
	else:
		in_file = '/home/priyanka/15618/scanner/examples/clip.mp4'
		out_file = '/home/priyanka/15618/scanner/examples/detected_faces.avi'

	capture = cv2.VideoCapture(in_file)
	width = int(capture.get(3))
	height = int(capture.get(4))
	writer = cv2.VideoWriter(out_file, H264_FOURCC, OUTPUT_FRAMERATE, (width, height))

	i = 1
	t0 = time.time()
	while(capture.isOpened()):
		ret, frame = capture.read()
		if ret==False:
			break
		result = process_frame(frame)
		writer.write(result)
		print('Processed frame-%s' % (i))
		i = i + 1
	t1 = time.time()

	print('\nTotal Time: {:.1f}s'.format(t1 - t0))
	speed = float(i-1) / float(t1-t0)
	print('\nProcessing Speed = %s' % (speed))
	cv2.destroyAllWindows()

run_everything()
