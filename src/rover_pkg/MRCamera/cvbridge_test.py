import cv2 as cv
import numpy as np
print(cv.__version__)

capture = cv.VideoCapture(0)
if not capture.isOpened():
    print("cannot open camera")
    exit()
while True:
    # capture frame-by-frame
    ret, frame = capture.read()

    # if fame is read correctly retis True
    if not ret:
        print("Cant recieve frame(stream end?). Exiting...")
        break
    #display frame
    cv.imshow('video', frame)
    if cv.waitKey(1) == ord('q'):
        break
# release capture and destroy windows
cap.release()
cv.destroyAllWindows()