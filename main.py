import cv2
import numpy as np
from PIL import ImageGrab
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import time


class ScreenRecorderApp(QMainWindow):
    def __init__(self):
        super(ScreenRecorderApp, self).__init__()

        self.setWindowTitle("Screen Recorder")
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel(self)
        self.label.setGeometry(10, 10, 780, 580)

        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(200, 530, 100, 30)
        self.start_button.clicked.connect(self.start_recording)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setGeometry(460, 530, 100, 30)
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.setEnabled(False)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.capture_frame)

        self.width = QApplication.desktop().screenGeometry().width()
        self.height = QApplication.desktop().screenGeometry().height()

        self.file_name = f"video\\video_{str(time.strftime('%d-%m-%Y-%H-%M-%S'))}.mp4"

        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.captured_video = None

    def start_recording(self):
        self.captured_video = cv2.VideoWriter(self.file_name, self.fourcc, 20.0, (self.width, self.height))
        self.timer.start(50)  # Capture a frame every 50 milliseconds
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_recording(self):
        self.timer.stop()
        self.captured_video.release()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def capture_frame(self):
        img = ImageGrab.grab(bbox=(0, 0, self.width, self.height))
        np_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        self.captured_video.write(np_img)

        # Convert the frame to QImage and display it in QLabel
        q_img = QImage(np_img.data, self.width, self.height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.label.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication([])
    recorder_app = ScreenRecorderApp()
    recorder_app.show()
    app.exec_()
