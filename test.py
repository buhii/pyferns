import cv, cv2
from numpy import array, int32
from pyferns import planar_pattern_detector_wrapper as FernsDetector

FLAG_INIT = False
REGION_THICKNESS = 6
IMG_NAME = "millet"

# --- initialize
fd1 = FernsDetector()
#fd2 = FernsDetector()

if FLAG_INIT:
    fd1.learn(IMG_NAME + ".jpg")
    fd1.save(IMG_NAME + ".doi")
else:
    fd1.just_load("monet.doi")
    #fd2.just_load("millet.doi")

# --- main

cv.NamedWindow("camera", 1)
capture = cv.CreateCameraCapture(0)
width = 960
height = 720

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
    cv.Line(img, pt1, pt2, color, REGION_THICKNESS)
    cv.Line(img, pt2, pt3, color, REGION_THICKNESS)
    cv.Line(img, pt3, pt4, color, REGION_THICKNESS)
    cv.Line(img, pt4, pt1, color, REGION_THICKNESS)


def check_convex(v):
    # return point array if contour is convex.
    # or return None
    contour = array([
            [[v[0], v[1]]],
            [[v[2], v[3]]],
            [[v[4], v[5]]],
            [[v[6], v[7]]]
            ],
            dtype=int32)
    if cv2.isContourConvex(contour):
        return v
    else:
        return None


while True:
    img = cv.QueryFrame(capture)
    # image = DetectRedEyes(img, faceCascade, eyeCascade)
    gray = cv.CreateImage((width, height), 8, 1)
    # Convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)

    # detect
    results = [fd1.detect(gray)] # [fd1.detect(gray), fd2.detect(gray)]
    results = map(lambda area: check_convex(area), results)

    for detect_color in zip(results, [RED, BLUE]):
        detect, color = detect_color
        if detect:
            draw_region(gray, detect, color)

    cv.ShowImage("camera", gray)
    k = cv.WaitKey(10);
    if k == 'f':
        break
