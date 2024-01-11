import queue
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer

from receive_frame import ReceiveFrame


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        
        self.frame_queue = queue.Queue(maxsize=30)    # 프레임이 저장될 큐
        self.startThread()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.camViewer)
        self.timer.start(30)

    def initUI(self):
        # UI 틀 만들기
        self.setWindowTitle('BTS')
        widget = QWidget()
        self.setCentralWidget(widget)
        
        vbox = QVBoxLayout(widget)
        
        pixmap = QPixmap('./class_diagram.png')
        self.lbl_img = QLabel()
        self.lbl_img.setPixmap(pixmap)
        
        lbl_size = QLabel('Hi')
        lbl_size.setAlignment(Qt.AlignCenter)
        
        vbox.addWidget(self.lbl_img)
        vbox.addWidget(lbl_size)
        self.setLayout(vbox)

        self.move(1000, 600)
        self.show()
        
    def startThread(self):
        self.video_thread = ReceiveFrame(self.frame_queue)
        self.video_thread.start()
        
    def camViewer(self):
        if self.frame_queue:
            frame = self.frame_queue.get()
            
            # 프레임 크기 확인
            height, width, channels = frame.shape
            bytes_per_line = channels * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_BGR888)
            
            if q_img:
                pixmap = QPixmap.fromImage(q_img)
                self.lbl_img.setPixmap(pixmap)
            else:
                print("Invalid Image Data")
                
    def closeThread(self, event):
        self.video_thread.quit()
        self.video_thread.wait()
        event.accept()