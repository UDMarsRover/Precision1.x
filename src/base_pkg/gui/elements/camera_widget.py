import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
import time
import threading
import os
from numpy import float64
from PIL import Image
import piexif
import glob
import time
import rospy
from std_msgs.msg import Float32

################################################
# IMPORTANT
#
# if using Linux, need to do "pip install opencv-python-headless" rather than "pip install opencv-python" because
# opencv and QT5 have some compatibility issues in Linux
################################################

class CameraWidget(QWidget):
    def __init__(self, camera_url=0, width=640, height=480):
        super().__init__()
        self.title = 'http Video Stream'
        self.left, self.top, self.width, self.height = 0, 0, width, height
        self.camera_url = camera_url
        self.lat = float64(0)
        self.lon = float64(0)
        self.setStyleSheet("background-color: black;")
        self.initUI()
        self.run()
        rospy.init_node("udmrt_camera_node", anonymous=True) 
        self.pub = rospy.Publisher("/pi/camera/servo", Float32, queue_size=10) 

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMaximumSize(self.width, self.height)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: grey;")

        # Create a label to display the video stream
        self.label = QLabel(self)
        # self.label.setGeometry(0, 0, self.width, self.height)
        # self.label.setContentsMargins(0, 0, 0, 0)

        # Create a camera control layout
        self.camera_control_layout = QHBoxLayout()


        # Create a capture button widget
        self.capture_button = QPushButton("Capture", self)
        self.capture_button.clicked.connect(self.capture_image)
        self.camera_control_layout.addWidget(self.capture_button)

        # Create a pano button widget
        self.capture_button = QPushButton("Pano", self)
        self.capture_button.clicked.connect(self.pano_image)
        self.camera_control_layout.addWidget(self.capture_button)

        # Create a button to open file explorer
        self.open_button = QPushButton("Select Directory", self)
        self.open_button.clicked.connect(self.open_image)
        self.camera_control_layout.addWidget(self.open_button)

        self.layout.addWidget(self.label)
        self.layout.addLayout(self.camera_control_layout)
        self.setLayout(self.layout)

        # Set up the video capture
        # self.cap = cv2.VideoCapture('http://192.168.8.121:5000')  # Replace with your actual video stream URL
        self.cap = cv2.VideoCapture(self.camera_url) # Replace with your actual video stream URL

    def set_camera_url(self, camera_url):
        self.stop_camera_thread()
        self.camera_url = camera_url
        self.cap = cv2.VideoCapture(self.camera_url)
        self.start_camera_thread()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb_image = frame
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(convert_to_qt_format)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio)
            self.label.setPixmap(pixmap)

    def run(self):
        self.start_camera_thread()
    def start_camera_thread(self):
        self.camera_thread = threading.Thread(target=self.update_stream)
        self.keep_streaming = True
        self.camera_thread.start()

    def closeEvent(self, event):
        self.stop_camera_thread()
        self.camera_thread.join()
        event.accept()

    def stop_camera_thread(self):
        
        self.keep_streaming = False
        self.camera_thread.join()
        self.cap.release()
        
    

    def update_stream(self):
        while self.keep_streaming:
            # print()
            self.update_frame()
            time.sleep(0.03)

    def capture_image(self):
        # Read a frame from the webcam
        ret, frame = self.cap.read()

        if ret:
            # Save the frame as an image file
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Go through the directory, incrementing a number to see if the directory has that file name
            file_name = "captured_image.jpg"
            i = 1
            while True:
                file_name = f"captured_image_{i}.jpg"
                if not os.path.exists(os.path.join(self.image_path, file_name)):
                    break
                i += 1

            # Save the frame as an image file with the unique file name
            # cv2.imwrite(os.path.join(self.image_path, file_name), frame)
            # Open the captured image using PIL
            # Convert the OpenCV image to PIL image
            image = Image.fromarray(frame)

            # image = Image.open(os.path.join(self.image_path, file_name))

            gps_ifd = {
                piexif.GPSIFD.GPSLatitudeRef: 'N' if self.lat >= 0 else 'S',
                piexif.GPSIFD.GPSLatitude: self.convert_to_exif_gps(abs(self.lat)),
                piexif.GPSIFD.GPSLongitudeRef: 'E' if self.lon >= 0 else 'W',
                piexif.GPSIFD.GPSLongitude: self.convert_to_exif_gps(abs(self.lon)),
            }
            
            exif_dict = {"GPS": gps_ifd}
            exif_bytes = piexif.dump(exif_dict)

            # Update the image with the GPS EXIF data
            image.save(os.path.join(self.image_path, file_name), format='JPEG', exif=exif_bytes)



            # Save the image with the updated GPS info
            # image.save(os.path.join(self.image_path, file_name), format='JPEG', exif=data_bytes)

    def convert_to_exif_gps(self, coord):
        """Convert a float coordinate to EXIF GPS format."""
        degrees = int(coord)
        minutes = int((coord - degrees) * 60)
        seconds = (coord - degrees - minutes / 60) * 3600
        return [(degrees, 1), (minutes, 1), (int(seconds * 100), 100)]

    def pano_image(self):
        frames = 10
        increment = 180 / frames
        angle = -90
        self.pub.publish(angle) #sets camera to -90
        time.sleep(2)
    #Capture images
        for i in range(0, frames):
            
            angle = angle + increment
            self.pub.publish(angle)
            time.sleep(2)

            # Read a frame from the webcam
            ret, frame = self.cap.read()

            if ret:
                # Save the frame as an image file
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Go through the directory, incrementing a number to see if the directory has that file name
                file_name = "captured_image.jpg"
                i = 1
                while True:
                    file_name = f"captured_image_{i}.jpg"
                    if not os.path.exists(os.path.join(self.image_path, file_name)):
                        break
                    i += 1

                # Save the frame as an image file with the unique file name
                # cv2.imwrite(os.path.join(self.image_path, file_name), frame)
                # Open the captured image using PIL
                # Convert the OpenCV image to PIL image
                image = Image.fromarray(frame)

                # image = Image.open(os.path.join(self.image_path, file_name))

                gps_ifd = {
                    piexif.GPSIFD.GPSLatitudeRef: 'N' if self.lat >= 0 else 'S',
                    piexif.GPSIFD.GPSLatitude: self.convert_to_exif_gps(abs(self.lat)),
                    piexif.GPSIFD.GPSLongitudeRef: 'E' if self.lon >= 0 else 'W',
                    piexif.GPSIFD.GPSLongitude: self.convert_to_exif_gps(abs(self.lon)),
                }
                
                exif_dict = {"GPS": gps_ifd}
                exif_bytes = piexif.dump(exif_dict)

                # Update the image with the GPS EXIF data
                image.save(os.path.join(self.image_path, file_name), format='JPEG', exif=exif_bytes)



                # Save the image with the updated GPS info
                # image.save(os.path.join(self.image_path, file_name), format='JPEG', exif=data_bytes)
    #Stitch images
        image_paths = glob.glob("src/base_pkg/gui/elements/panoImg/*.jpg")
        images = []

        for image in image_paths:
            img = cv2.imread(image)
            images.append(img)

        imageStitcher = cv2.Stitcher_create()

        error, stitched_img = imageStitcher.stitch(images)

        #if error: 
        #    print("sad")
        #    print(error)

        if not error:

            cv2.imwrite("src/base_pkg/gui/elements/panoImg/stitchedOutput.jpg", stitched_img)
            cv2.waitKey(0)

    def open_image(self):
        # Open a file dialog to select an image file
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        if dialog.exec_():
            self.image_path = dialog.selectedFiles()[0]
        print(self.image_path)

    def set_gps_coords(self, lat, lon):
        self.lat = lat
        self.lon = lon




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraWidget(width=1280, height=720)

    print("SHOWING")
    ex.show()
    sys.exit(app.exec_())
