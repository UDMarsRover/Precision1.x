import cv2 as cv
print(cv.__version__)

capture = cv.VideoCapture(1)
if not capture.isOpened():
    print("cannot open camera")
    exit()
while True:
    # capture frame-by-frame
    ret, frame = capture.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Cant recieve frame(stream end?). Exiting...")
        break
    #display frame
    cv.imshow('video', frame)
    if cv.waitKey(1) == ord('q'):
        break
# release capture and destroy windows
capture.release()
cv.destroyAllWindows()