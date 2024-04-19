from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QLabel
 
import rospy
from std_msgs.msg import String


class ErrorBoxes(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(ErrorBoxes, self).__init__(*args, **kwargs)

        layout = QtWidgets.QHBoxLayout()
        self.setFixedSize(QSize(600, 200))

        emoError = True
        driveError = False
        armError = False
        camError = False
      
        emoLabel = QLabel("Emo Error")
        if(emoError):
            emoLabel.setStyleSheet("background-color: red; color: white;")
        else:
            emoLabel.setStyleSheet("background-color: white; color: white;")
        emoLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(emoLabel)

        driveLabel = QLabel("Drive Error")
        if(driveError):
            driveLabel.setStyleSheet("background-color: red; color: white;")
        else:
            driveLabel.setStyleSheet("background-color: white; color: white;")
        driveLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(driveLabel)

        armLabel = QLabel("Arm Error")
        if(armError):
            armLabel.setStyleSheet("background-color: red; color: white;")
        else:
            armLabel.setStyleSheet("background-color: white; color: white;")
        armLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(armLabel)

        camLabel = QLabel("Camera Error")
        if(camError):
            camLabel.setStyleSheet("background-color: red; color: white;")
        else:
            camLabel.setStyleSheet("background-color: white; color: white;")
    
        camLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(camLabel)
 
        self.setLayout(layout)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    volume = ErrorBoxes()
    volume.show()
    app.exec_()
    


class Roser:

    def callback(data):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

    def listener():

        # In ROS, nodes are uniquely named. If two nodes with the same
        # name are launched, the previous one is kicked off. The
        # anonymous=True flag means that rospy will choose a unique
        # name for our 'listener' node so that multiple listeners can
        # run simultaneously.
        rospy.init_node('listener', anonymous=True)

        rospy.Subscriber('chatter', String)

        # spin() simply keeps python from exiting until this node is stopped

        rospy.spin

    if __name__ == "__main__":
        listener()
            

