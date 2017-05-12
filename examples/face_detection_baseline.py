import sys, os
matt = "MATT" in os.environ
if not matt:
    sys.path.append("/home/priyanka/15618/scanner")
import time
import cv2
import numpy as np



OUTPUT_FRAMERATE = 24
H264_FOURCC = cv2.VideoWriter_fourcc(*"h264")
face_cascade = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")


def face_detector(image):
	grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	faces = face_cascade.detectMultiScale(grayscale, 1.3, 5)
	coords = []
	for (x, y, w, h) in faces:
		coords.extend([x, y, w, h])
	return np.asarray(coords, dtype='int64')

def draw_boxes(img, coords):
	for i in range(0, len(coords), 4):
		x, y, w, h = coords[i:i+4]
		img = cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2)
	return img

def process_frame(frame):
	bounding_box = face_detector(frame)
	out_frame = draw_boxes(frame, bounding_box)
	return out_frame

# Read in the video
# Detect faces
# Draw bounding boxes
# Output the video with bounding boxes drawn on it

if matt:
	in_file = '?'
	out_file = '?'
else:
	in_file = '/home/priyanka/15618/scanner/examples/clip.mp4'
	out_file = '/home/priyanka/15618/scanner/examples/detected_faces.avi'

capture = cv2.VideoCapture(in_file)
width = int(capture.get(3))
height = int(capture.get(4))
writer = cv2.VideoWriter(out_file, H264_FOURCC, OUTPUT_FRAMERATE, (width, height))

i = 1
s = time.time()
while True:
    ret, img = capture.read()
    result = process_frame(img)
    writer.write(result[:, :, ::-1])
    if 0xFF & cv2.waitKey(5) == 27:
        break
    print('Processed frame-%s' % (i))
    i = i + 1
print('\nTotal Time: {:.1f}s'.format(time.time() - s))
cv2.destroyAllWindows()
