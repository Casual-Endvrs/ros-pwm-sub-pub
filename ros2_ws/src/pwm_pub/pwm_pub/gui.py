import sys
from PyQt5 import QtGui

from PyQt5.Qt import Qt
from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QTabWidget,
    QGroupBox,
    QRadioButton,
    QSlider,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QComboBox,
    QTextEdit,
    QFileDialog,
    QLineEdit,
    QStyleOptionSlider,
    QStyle,
    QCheckBox,
)

from PyQt5.QtGui import QKeyEvent

import rclpy
from rclpy.executors import MultiThreadedExecutor

from threading import Thread

from PWM_Publisher import PWM_Publisher

class App(QMainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setWindowTitle("RC Car Controller")

        # Start - Node control
        self.node = PWM_Publisher()
        self.executor = MultiThreadedExecutor()
        self.executor.add_node(self.node)
        self.node_thread = Thread(target=self.executor.spin)
        self.node_thread.start()
        self.node.get_logger().info("Spinned ROS2 Node . . .")
        # End - Node control

        self.pressed_keys = set()

        self.table_widget = QWidget()
        self.setCentralWidget(self.table_widget)

        self.show()

    def keyPressEvent(self, event):
        if event.isAutoRepeat() :
            return
        
        if event.text() in self.pressed_keys :
            return
    
        if event.text().isalpha() :
            self.pressed_keys.add(event.text().lower())

            if event.text() == 'w' :
                self.node.action[0] = 1
            elif event.text() == 's' :
                self.node.action[0] = -1
            elif event.text() == 'a' :
                self.node.action[1] = -1
            elif event.text() == 'd' :
                self.node.action[1] = 1
    
    def keyReleaseEvent(self, event):
        if event.isAutoRepeat() :
            return
        
        if event.text() in self.pressed_keys :
            self.pressed_keys.remove(event.text().lower())

            if event.text() in ['w', 's'] :
                self.node.action[0] = 0
            elif event.text() in ['a', 'd'] :
                self.node.action[1] = 0
    
    def __del__(self):
        print("--- exiting ---")
        self.node.destroy_node()
        self.executor.shutdown()


def main(args=None):
        rclpy.init(args=args)

        app = QApplication(sys.argv)
        app.setStyle("Fusion")

        window = App()
        sys.exit(app.exec_())
        rclpy.shutdown()


if __name__ == "__main__":
    main()




