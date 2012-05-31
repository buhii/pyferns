import cv
from pyferns import planar_pattern_detector_wrapper as FernsDetector
FLAG_INIT = False

IMG_NAME = "semiotics"
# IMG_NAME = "monet"

# --- initialize
fd = FernsDetector()
if FLAG_INIT:
    fd.learn(IMG_NAME + ".jpg")
    fd.save(IMG_NAME + ".doi")
else:
    fd.just_load(IMG_NAME + ".doi")

# --- main

cv.NamedWindow("camera", 1)
capture = cv.CreateCameraCapture(0)

width = None
height = None
width = 640
height = 480

if width is None:
    width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
else:
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)

if height is None:
    height = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT))
else:
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height)

result = cv.CreateImage((width,height),cv.IPL_DEPTH_8U,3)

while True:
    img = cv.QueryFrame(capture)
    # image = DetectRedEyes(img, faceCascade, eyeCascade)
    gray = cv.CreateImage((width, height), 8, 1)
    # Convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)
    cv.ShowImage("camera", gray)

    print fd.detect(gray)
    k = cv.WaitKey(10);
    if k == 'f':
        break
