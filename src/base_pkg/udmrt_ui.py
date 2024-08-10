import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout
from gui.elements.error_status_panel import ErrorStatusPanel
from gui.elements.camera_widget import CameraWidget
from gui.lidar.lidar_widget import LidarWidget
from sensor_msgs.msg import LaserScan, BatteryState, NavSatFix, Temperature, Range
#import random
from PyQt5.QtWidgets import QDial, QLabel, QVBoxLayout, QWidget, QStackedLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
#import rssi
from PyQt5.QtWidgets import QComboBox
import threading
import rospy
GUI_WIDTH = 2800
GUI_HEIGHT = 1600
CAMERA_URLs = [0, "http://192.168.8.223:8080"]
CAMERA_NAMES = ["WebCam", "Main Camera", "Arm Camera"]
MAX_SPEED = 6
SONAR_RANGE_GOOD = 1.5
SONAR_RANGE_WARNING = 0.5
LIDAR_MAX_RANGE = 4.0

BATTERY_STATE_TOPIC = "/emo/batteryVoltage"
GPS_DATA_TOPIC = "/emo/gps"
BATTERY_TEMP_TOPIC = "/emo/batteryTemperature"
VOLTAGE_CONVERTER_TEMP_TOPIC = "/emo/voltageConverterTemperature"
BOX_TEMP_TOPIC = "/emo/boxTemperature"
SONAR_NW_TOPIC = "/emo/ultraNW"
SONAR_NE_TOPIC = "/emo/ultraNE"
SONAR_SW_TOPIC = "/emo/ultraSW"
SONAR_SE_TOPIC = "/emo/ultraSE"
ros_controller = None

class MyWindow(QWidget):
    def __init__(self, width, height):
        super().__init__()
        global GUI_WIDTH
        global GUI_HEIGHT
        GUI_WIDTH = width
        GUI_HEIGHT = height
        global ros_controller
        ros_controller = ROSMagic()
        
        self.initUI()
    def initUI(self):
        self.setWindowTitle('UDMRT')
        self.layout = QHBoxLayout()
        
        self.layout.addWidget(self.init_error_panel())
        self.info_panel = InfoPanel()
        self.layout.addWidget(self.info_panel)
        self.setLayout(self.layout)
        self.show()

    def init_error_panel(self):
        error_panel = ErrorStatusPanel()
        pi_error_box = error_panel.add_error()
        pi_error_box.set_name("Pi")

        emo_error_box = error_panel.add_error()
        emo_error_box.set_name("EMO")

        drive_error_box = error_panel.add_error()
        drive_error_box.set_name("Drive")
        
        arm_error_box = error_panel.add_error()
        arm_error_box.set_name("Arm")

        camera_error_box = error_panel.add_error()
        camera_error_box.set_name("Camera")
    
        # for i in range(5):
        #     error_box = error_panel.add_error()
        #     error_box.set_name(f"Error {i}")
        #     error_box.set_id(i)
        #     error_box.set_status(random.randint(0, 3))
        #     for i in range(20):
        #         error_box.new_error(f"This is an error message ({i})")
        return error_panel
    
    def closeEvent(self, event):
        self.info_panel.camera_lidar_widget.close_camera()
        event.accept()

class CameraLidarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('UDMRT')
        self.layout = QHBoxLayout()
        self.camera_layout = QVBoxLayout()
        self.dropdown = QComboBox()
        for name in CAMERA_NAMES:
            self.dropdown.addItem(name)

        self.camera_layout.addWidget(self.dropdown)
        self.camera_widget = CameraWidget(CAMERA_URLs[0], int(GUI_WIDTH*0.4), int(GUI_HEIGHT*0.4))
        self.camera_widget.set_camera_url(0)
        self.camera_layout.addWidget(self.camera_widget)
        self.dropdown.currentIndexChanged.connect(self.camera_selected)
        self.layout.addLayout(self.camera_layout)
        self.distance_layout = QGridLayout()
        self.distance_layout.setHorizontalSpacing(10)
        self.distance_layout.setVerticalSpacing(10)
        self.distance_layout.setContentsMargins(10, 10, 10, 10)
        self.distance_layout.setAlignment(Qt.AlignCenter)
        lidar_widget = LidarWidget(LIDAR_MAX_RANGE, int(GUI_WIDTH*0.2))
        ros_controller.add_ros_subscriber("scan", LaserScan, lidar_widget.ros_callback)
        self.distance_layout.addWidget(lidar_widget, 1, 1)
        self.sonar_circles()
        self.layout.addLayout(self.distance_layout)
        self.setLayout(self.layout)
        self.setMinimumWidth(int(GUI_WIDTH * 0.8))
        self.setMinimumHeight(GUI_HEIGHT * 0.3)

    def camera_selected(self, index):
        self.camera_widget.set_camera_url(CAMERA_URLs[index])

    def sonar_circles(self):
        self.circle_nw = CircleWidget()
        self.circle_ne = CircleWidget()
        self.circle_sw = CircleWidget()
        self.circle_se = CircleWidget()
        self.distance_layout.addWidget(self.circle_nw, 0, 0)
        self.distance_layout.addWidget(self.circle_ne, 0, 2)
        self.distance_layout.addWidget(self.circle_sw, 2, 0)
        self.distance_layout.addWidget(self.circle_se, 2, 2)
        range_empty = Range()
        range_empty.range = 0.0
        self.sonar_nw_callback(range_empty)
        self.sonar_ne_callback(range_empty)
        self.sonar_sw_callback(range_empty)
        self.sonar_se_callback(range_empty)
        ros_controller.add_ros_subscriber(SONAR_NW_TOPIC, Range, self.sonar_nw_callback)
        ros_controller.add_ros_subscriber(SONAR_NE_TOPIC, Range, self.sonar_ne_callback)
        ros_controller.add_ros_subscriber(SONAR_SW_TOPIC, Range, self.sonar_sw_callback)
        ros_controller.add_ros_subscriber(SONAR_SE_TOPIC, Range, self.sonar_se_callback)

    def sonar_nw_callback(self, range_msg):
        range = range_msg.range
        self.circle_nw.set_text(f"{range:.2f}m")
        if range > SONAR_RANGE_GOOD:
            self.circle_nw.set_color(Qt.green)
        elif range > SONAR_RANGE_WARNING:
            self.circle_nw.set_color(Qt.yellow)
        else:
            self.circle_nw.set_color(Qt.red)   

    def sonar_ne_callback(self, range_msg):
        range = range_msg.range
        self.circle_ne.set_text(f"{range:.2f}m")
        if range > SONAR_RANGE_GOOD:
            self.circle_ne.set_color(Qt.green)
        elif range > SONAR_RANGE_WARNING:
            self.circle_ne.set_color(Qt.yellow)
        else:
            self.circle_ne.set_color(Qt.red)

    def sonar_sw_callback(self, range_msg):
        range = range_msg.range
        self.circle_sw.set_text(f"{range:.2f}m")
        if range > SONAR_RANGE_GOOD:
            self.circle_sw.set_color(Qt.green)
        elif range > SONAR_RANGE_WARNING:
            self.circle_sw.set_color(Qt.yellow)
        else:
            self.circle_sw.set_color(Qt.red)

    def sonar_se_callback(self, range_msg):
        range = range_msg.range
        self.circle_se.set_text(f"{range:.2f}m")
        if range > SONAR_RANGE_GOOD:
            self.circle_se.set_color(Qt.green)
        elif range > SONAR_RANGE_WARNING:
            self.circle_se.set_color(Qt.yellow)
        else:
            self.circle_se.set_color(Qt.red)     

    def close_camera(self):
        self.camera_widget.close()

class InfoPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('UDMRT')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.camera_lidar_widget = CameraLidarWidget()
        self.layout.addWidget(self.camera_lidar_widget)
        self.status_panel = StatusPanel()
        self.layout.addWidget(self.status_panel)
        self.rover_abs_panel = RoverAbsPanel()
        self.layout.addWidget(self.rover_abs_panel)

class RoverAbsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.setStyleSheet("border: 10px solid black;")
        self.signal_strength_label = QLabel()
        self.pitch_label = QLabel()
        self.roll_label = QLabel()
        self.layout.addWidget(self.signal_strength_label)
        self.layout.addWidget(self.pitch_label)
        self.layout.addWidget(self.roll_label)
        self.setLayout(self.layout)
        self.wifi_signal_strength_callback("-89db")
        self.pitch_callback(0.0)
        self.roll_callback(0.0)
        self.setMaximumHeight(GUI_HEIGHT * 0.05)

    def wifi_signal_strength_callback(self, signal_strength):
        self.signal_strength_label.setText(f"Signal Strength: {signal_strength}")

    def pitch_callback(self, pitch):
        self.pitch_label.setText(f"Pitch: {pitch}")

    def roll_callback(self, roll):  
        self.roll_label.setText(f"Roll: {roll}")


class StatusPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.battery_status_widget = BatteryStatusWidget()
        self.layout.addWidget(self.battery_status_widget)
        self.gps_widget = GPSDataWidget()
        self.layout.addWidget(self.gps_widget)
        self.speed_widget = SpeedWidget()
        self.layout.addWidget(self.speed_widget)
        self.temperature_widget = TemperatureWidget()
        self.layout.addWidget(self.temperature_widget)

class BatteryStatusWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.label = QLabel("Battery Status")
        self.layout.addWidget(self.label)
        self.data_label = QLabel()
        self.layout.addWidget(self.data_label)
        self.data_label.setStyleSheet("font-size: 60px;")
        self.battery_status_callback(0.0)
        ros_controller.add_ros_subscriber(BATTERY_STATE_TOPIC, BatteryState, self.battery_status_callback)
        
    def battery_status_callback(self, voltage):
        self.data_label.setText(f"{voltage}V")

class GPSDataWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.lat_label = QLabel()
        self.layout.addWidget(self.lat_label)
        self.long_label = QLabel()
        self.layout.addWidget(self.long_label)
        empty_msg = NavSatFix()
        empty_msg.latitude = 0.0000014
        empty_msg.longitude = 0.00013
        self.gps_data_callback(empty_msg)
        ros_controller.add_ros_subscriber(GPS_DATA_TOPIC, NavSatFix, self.gps_data_callback)
        
    def gps_data_callback(self, navsatfix_msg):
        
        self.lat_label.setText(f"{round(navsatfix_msg.latitude, 10):.10f} N")
        self.long_label.setText(f"{round(navsatfix_msg.longitude, 10):.10f} W")

class SpeedWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.speed_label = QLabel()
        self.speed_label.setStyleSheet("font-size: 60px;")
        self.speed_label.setAlignment(Qt.AlignCenter)
        self.speed_dial = QDial()
        self.speed_dial.setNotchesVisible(True)
        self.speed_dial.setEnabled(False)
        self.speed_dial.setRange(0, MAX_SPEED)
        self.layout.addWidget(self.speed_label)
        self.layout.addWidget(self.speed_dial)
        self.update_speed_label(0)
        #  Add a ros subscriber for speed data
        
    def update_speed_label(self, value):
        self.speed_dial.setValue(value)
        self.speed_label.setText(f"{value:.2f} mph")


class TemperatureWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.battery_temp_label = QLabel("Battery Temp")
        self.battery_temp_label.setStyleSheet("font-weight: bold;")
        self.layout.addWidget(self.battery_temp_label)
        self.battery_temp_data_label = QLabel()
        self.layout.addWidget(self.battery_temp_data_label)

        self.voltage_converter_temp_label = QLabel("Voltage Converter Temp")
        self.voltage_converter_temp_label.setStyleSheet("font-weight: bold;")
        self.layout.addWidget(self.voltage_converter_temp_label)
        self.voltage_converter_temp_data_label = QLabel()
        self.layout.addWidget(self.voltage_converter_temp_data_label)

        self.box_temp_label = QLabel("Box Temp")
        self.box_temp_label.setStyleSheet("font-weight: bold;")
        self.layout.addWidget(self.box_temp_label)
        self.box_temp_data_label = QLabel()
        self.layout.addWidget(self.box_temp_data_label)
        temperature_empty_msg = Temperature()
        temperature_empty_msg.temperature = 0.0
        self.battery_temperature_callback(temperature_empty_msg)
        self.voltage_converter_temperature_callback(temperature_empty_msg)
        self.box_temperature_callback(temperature_empty_msg)
        ros_controller.add_ros_subscriber(BATTERY_TEMP_TOPIC, Temperature, self.battery_temperature_callback)
        ros_controller.add_ros_subscriber(VOLTAGE_CONVERTER_TEMP_TOPIC, Temperature, self.voltage_converter_temperature_callback)
        ros_controller.add_ros_subscriber(BOX_TEMP_TOPIC, Temperature, self.box_temperature_callback)
        
    def battery_temperature_callback(self, temperature_msg):
        self.battery_temp_data_label.setText(f"{temperature_msg.temperature:.2f}°C")
    
    def voltage_converter_temperature_callback(self, temperature_msg):
        self.voltage_converter_temp_data_label.setText(f"{temperature_msg.temperature:.2f}°C")

    def box_temperature_callback(self, temperature_msg):
        self.box_temp_data_label.setText(f"{temperature_msg.temperature:.2f}°C")
    

class ROSMagic:
    def __init__(self):
        self.subscribers = []

    def start_ros_thread(self):
        rospy.init_node("udmrt_gui_node", anonymous=True)
        self.ros_thread = threading.Thread(target=self.update_from_ros)
        self.ros_thread.start()

    def update_from_ros(self):
        for subscriber in self.subscribers:
            ros_subscriber = rospy.Subscriber(subscriber["topic"], subscriber["datatype"], subscriber["callback"])
        rospy.spin()

    """Add a ROS subscriber to the GUI. The callback function will be called when a message is received."""
    def add_ros_subscriber(self, topic, callback, datatype):
        self.subscribers.append({"topic":topic, "datatype":datatype, "callaback":callback})
        None
        
class CircleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(int(GUI_WIDTH * 0.05), int(GUI_HEIGHT * 0.05))
        self.setMaximumSize(int(GUI_WIDTH * 0.05), int(GUI_HEIGHT * 0.05))
        self.text = ""
        self.color = Qt.gray

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 10, 10)

        font = painter.font()
        font.setPointSize(12)
        painter.setFont(font)
        painter.setPen(Qt.black)
        painter.drawText(event.rect(), Qt.AlignCenter, self.text)

    def set_size(self, width, height):
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)

    def set_text(self, text):
        self.text = text
        self.update()

    def set_color(self, color):
        self.color = color
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    screen_width, screen_height = screen_resolution.width(), screen_resolution.height()

    window = MyWindow(screen_width, screen_height)
    sys.exit(app.exec_())