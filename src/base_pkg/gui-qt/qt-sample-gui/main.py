# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit
# app = QApplication([])
# window = QWidget()
# layout = QVBoxLayout()

# text_box = QLineEdit()
# layout.addWidget(text_box)
# enter_button = QPushButton('Clear')
# enter_button.clicked.connect(lambda: clear())
# layout.addWidget(enter_button)
# text_box.returnPressed.connect(lambda: on_enter()) 


# def on_enter():
#     print(text_box.text())

# def clear():
#     text_box.setText("")

# window.setLayout(layout)
# window.show()
# app.exec()

# from PyQt5 import QtWidgets
# from PyQt5.QtGui import QImage,QPixmap
# from PyQt5.QtCore import QThread,pyqtSignal as Signal,pyqtSlot as Slot
# import cv2,imutils
# # pip install imutils
# import sys

# class MyThread(QThread):
#     frame_signal = Signal(QImage)

#     def run(self):
#         self.cap = cv2.VideoCapture()
#         self.cap.open
#         while self.cap.isOpened():
#             _,frame = self.cap.read()
#             frame = self.cvimage_to_label(frame)
#             self.frame_signal.emit(frame)
    
#     def cvimage_to_label(self,image):
#         image = imutils.resize(image,width = 640)
#         image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
#         image = QImage(image,
#                        image.shape[1],
#                        image.shape[0],
#                        QImage.Format_RGB888)
#         return image

# class MainApp(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.init_ui()
#         self.show()
    
#     def init_ui(self):
#         self.setFixedSize(640,640)
#         self.setWindowTitle("Camera FeedBack")

#         widget = QtWidgets.QWidget(self)

#         layout = QtWidgets.QVBoxLayout()
#         widget.setLayout(layout)

#         self.label = QtWidgets.QLabel()
#         layout.addWidget(self.label)

#         self.open_btn = QtWidgets.QPushButton("Open The Camera", clicked=self.open_camera)
#         layout.addWidget(self.open_btn)

#         self.camera_thread = MyThread()
#         self.camera_thread.frame_signal.connect(self.setImage)

#         self.setCentralWidget(widget)
    
#     def open_camera(self):        
#         self.camera_thread.start()
#         print(self.camera_thread.isRunning())

#     @Slot(QImage)
#     def setImage(self,image):
#         self.label.setPixmap(QPixmap.fromImage(image))



# if __name__ == "__main__":
#     app = QtWidgets.QApplication([])
#     main_window = MainApp()
#     sys.exit(app.exec())


# import the opencv library 
import cv2 
  
  
# define a video capture object 
vid = cv2.VideoCapture(0) 
  
while(True): 
      
    # Capture the video frame 
    # by frame 
    ret, frame = vid.read() 
  
    # Display the resulting frame 
    cv2.imshow('frame', frame) 
      
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 