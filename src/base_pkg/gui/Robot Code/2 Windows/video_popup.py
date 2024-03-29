import numpy as np
import cv2 as cv


##################################################################################################
# THE NUMBER IN THE VIDEOCAPTURE() MAY NEED TO BE CHANGED DEPENDING ON THE DEVICE USING IT!!!!!
##################################################################################################
cap = cv.VideoCapture(1)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame

    # UNCOMMENT TO ALLOW WINDOW TO BE RESIZEABLE
    cv.namedWindow("Robot Camera", cv.WINDOW_AUTOSIZE)

    cv.imshow("Robot Camera", frame)
    cv.setWindowProperty("Robot Camera", cv.WND_PROP_TOPMOST, 1)
    # cv.setWindowProperty('Robot Camera', cv.WND_PROP_ASPECT_RATIO, 0)

    if cv.waitKey(1) == ord("q"):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
