import cv2

import cv2.aruco as aruco

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Load the ArUco dictionary
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
parameters =  cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect ArUco markers
    corners, ids, rejected = detector.detectMarkers(frame)


    # Draw detected markers on the frame
    frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    # Print the content of each detected marker
    if ids is not None:
        for i in range(len(ids)):
            print("Detected marker with ID:", ids[i], "Content:", dictionary[ids[i][0]])

    # Show the frame
    cv2.imshow('Webcam', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()