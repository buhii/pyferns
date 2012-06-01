import cv
from pyferns import planar_pattern_detector_wrapper as FernsDetector
FLAG_INIT = False

IMG_NAME = "semiotics"
# IMG_NAME = "monet"

# --- initialize
fd1 = FernsDetector()

"""
fd2 = FernsDetector()
fd2.learn("millet.jpeg")
fd2.save("millet.doi")
"""

fd2 = FernsDetector()

if FLAG_INIT and False:
    fd1.learn(IMG_NAME + ".jpg")
    fd1.save(IMG_NAME + ".doi")
else:
    fd1.just_load("monet.doi")
    fd2.just_load("millet.doi")

# --- main

cv.NamedWindow("camera", 1)
capture = cv.CreateCameraCapture(0)
width = 640
height = 480

RED = cv.RGB(255, 0, 0)
BLUE = cv.RGB(0, 0, 255)

if width is None:
    width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
else:
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)

if height is None:
    height = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT))
else:
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height)

result = cv.CreateImage((width,height),cv.IPL_DEPTH_8U,3)


def draw_region(img, tpl, color):
    pt1, pt2, pt3, pt4 = zip(tpl[0::2], tpl[1::2])
    cv.Line(img, pt1, pt2, color)
    cv.Line(img, pt2, pt3, color)
    cv.Line(img, pt3, pt4, color)
    cv.Line(img, pt4, pt1, color)


while True:
    img = cv.QueryFrame(capture)
    # image = DetectRedEyes(img, faceCascade, eyeCascade)
    gray = cv.CreateImage((width, height), 8, 1)
    # Convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)

    # detect
    tpl = fd1.detect(gray)

    if filter(lambda i: i != 0, tpl):
        print tpl
        draw_region(gray, tpl, RED)

    tpl = fd2.detect(gray)

    if filter(lambda i: i != 0, tpl):
        print tpl
        draw_region(gray, tpl, BLUE)

    cv.ShowImage("camera", gray)
    k = cv.WaitKey(10);
    if k == 'f':
        break
