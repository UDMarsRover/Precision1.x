import sys
import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
import threading
import time

class WebcamWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Webcam Widget")
        self.image_label = QLabel(self)
        self.image_label.setMinimumSize(1280, 960)
        self.image_label.setAlignment(Qt.AlignCenter)
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_frame)
        # self.timer.start(30)  # Update frame every 30 milliseconds

    def update_frame(self, ret, frame):
        if ret:
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

class ArucoDetector():
    def __init__(self, camera_ui) -> None:
        self.camera_ui = camera_ui
        # Initialize the webcam
        self.cap = cv2.VideoCapture(0)

        # Load the ArUco dictionary
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
        self.parameters =  cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.dictionary, self.parameters)     

    def detect_markers(self):
        while True:
            # Read a frame from the webcam
            ret, frame = self.cap.read()

            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect ArUco markers
            corners, ids, rejected = self.detector.detectMarkers(gray)


            # Draw detected markers on the frame
            # frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            # Print the content of each detected marker
            if ids is not None:
                for i in range(len(ids)):
                    print("Detected marker with ID:", ids[i])
                    # Draw outline of the marker on the current frame
                    # Get the corners of the marker
                    marker_corners = corners[i][0]
                    marker_corners = marker_corners.astype(int)
                    # Draw the outline of the marker
                    cv2.polylines(frame, [marker_corners], True, (0, 255, 0), 2)
                    # Put the text of the ID in the middle of the tag in the frame
                    # Calculate the center of the marker
                    center_x = int((marker_corners[0][0] + marker_corners[2][0]) / 2)
                    center_y = int((marker_corners[0][1] + marker_corners[2][1]) / 2)

                    # Draw the ID text on the frame
                    cv2.putText(frame, str(ids[i]), (center_x, center_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            else:
                print("No markers detected")

            # Show the frame
            # cv2.imshow('Webcam', frame)
            self.camera_ui.update_frame(ret, frame)

            # Exit if 'q' is pressed
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
            time.sleep(0.06)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = WebcamWidget()
    detector = ArucoDetector(widget)
    detector_thread = threading.Thread(target=detector.detect_markers)
    detector_thread.start()
    widget.show()
    sys.exit(app.exec_())