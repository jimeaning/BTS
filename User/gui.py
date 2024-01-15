"""
GUI 모듈
"""
import queue
import pygame

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QFrame, QHBoxLayout, QTextEdit, QSizePolicy, QLCDNumber, QPushButton, QMenuBar,QStatusBar
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QCoreApplication, QUrl, QTimer, QDateTime, QRect, QSize, QMetaObject

from receive_frame import ReceiveFrame
from receiver import ReceiveMessage
from sender import SendMessage


class MainWindow(QMainWindow):
    """GUI 클래스"""
    def __init__(self):
        super().__init__()
        self.counter = 3 # 남은 탄 개수
        self.count_timer = 5  # 초기 타이머 남은 시간
        
        self.frame_queue = queue.Queue(maxsize=30)    # 프레임이 저장될 큐
        self.msg_queue = queue.Queue(maxsize=30)    # 메세지가 저장될 큐
        self.StartThread()
        
        self.timer_LCD = QTimer(self)
        self.timer_LCD.timeout.connect(self.UpdateCount)
                
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.CamViewer)
        self.timer.start(30)
        
        self.initUI()
        
    def initUI(self):        
        # Main window
        self.setWindowTitle('BTS')
        self.setObjectName("MainWindow")
        self.resize(800, 850)

        self.central_widget = QWidget()
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        # 웹캠이 들어갈 영역
        self.frame = QFrame(self.central_widget)
        self.frame.setGeometry(QRect(60, 20, 640, 480))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")

        # 콘솔, 타이머, 발사 버튼, 남은 탄 갯수에 대한 그룹화된 위젯
        self.horizontal_layoutWidget = QWidget(self.central_widget)
        self.horizontal_layoutWidget.setGeometry(QRect(60, 540, 640, 210))
        self.horizontal_layoutWidget.setObjectName("horizontal_layoutWidget")
        self.horizontal_layout = QHBoxLayout(self.horizontal_layoutWidget)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setObjectName("horizontal_layout") 
        
        # 콘솔 TextEdit
        self.console_box = QTextEdit(self.horizontal_layoutWidget)
        # self.console_box.setEnabled(False)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.console_box.sizePolicy().hasHeightForWidth())

        self.console_box.setSizePolicy(sizePolicy)
        self.console_box.setMaximumSize(QSize(300, 16777215))
        self.console_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.console_box.setReadOnly(True)
        self.console_box.setObjectName("console_box")

        self.horizontal_layout.addWidget(self.console_box)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setContentsMargins(60, -1, -1, -1)
        self.vertical_layout.setObjectName("vertical_layout")

        # 타이머 LCD
        self.lcd_number = QLCDNumber(self.horizontal_layoutWidget)
        self.lcd_number.setMaximumSize(QSize(16777215, 70))
        self.lcd_number.setObjectName("lcd_number")
        self.vertical_layout.addWidget(self.lcd_number)

        # 발사 버튼
        self.btn_launch = QPushButton(self.horizontal_layoutWidget)
        self.btn_launch.setEnabled(False)
        self.btn_launch.setObjectName("btn_launch")
        self.btn_launch.clicked.connect(self.BtnClicked)

        self.vertical_layout.addWidget(self.btn_launch)
        self.vertical_layout_2 = QVBoxLayout()
        self.vertical_layout_2.setObjectName("vertical_layout_2")
        self.horizontal_layout_2 = QHBoxLayout()
        self.horizontal_layout_2.setObjectName("horizontal_layout_2")

        # 남은 탄 개수 label
        self.label = QLabel(self.horizontal_layoutWidget)
        self.label.setObjectName("label")
        self.horizontal_layout_2.addWidget(self.label)

        # 숫자 label
        self.num_bullet = QLabel(self.horizontal_layoutWidget)
        self.num_bullet.setObjectName("num_bullet")

        _translate = QCoreApplication.translate
        self.btn_launch.setText(_translate("MainWindow", "발사"))
        self.label.setText(_translate("MainWindow", "남은 탄 개수 :"))
        self.num_bullet.setText(_translate("MainWindow", str(self.counter)))

        self.horizontal_layout_2.addWidget(self.num_bullet)
        self.vertical_layout_2.addLayout(self.horizontal_layout_2)
        self.vertical_layout.addLayout(self.vertical_layout_2)
        self.horizontal_layout.addLayout(self.vertical_layout)

        self.setCentralWidget(self.central_widget)

        self.menubar = QMenuBar()
        self.menubar.setGeometry(QRect(0, 0, 800, 28))
        self.menubar.setObjectName("menubar")

        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar()
        self.statusbar.setObjectName("statusbar")

        self.setStatusBar(self.statusbar)

        QMetaObject.connectSlotsByName(self)

        pixmap = QPixmap('image/supersonic.jpg')
        self.lbl_img = QLabel(self.frame)
        self.lbl_img.setPixmap(pixmap.scaled(640, 480))
            
        self.move(1000, 600)
        self.show()
        
    def StartThread(self):
        """Thread 동작 시작"""
        self.video_thread = ReceiveFrame(self.frame_queue)
        self.video_thread.start()        
        self.hw_thread = ReceiveMessage(self.msg_queue)
        self.hw_thread.rcv_msg_signal.connect(self.ConsoleMsg)
        self.hw_thread.start()
        
    def ShowTimeline(self):
        """console에 찍히는 현재 시간"""
        current_datetime = QDateTime.currentDateTime()
        formatted_datetime = current_datetime.toString("yyyy-MM-dd hh:mm:ss")

        return formatted_datetime

    def BtnClicked(self):
        """발사 버튼 클릭 시 이벤트"""
        sending = SendMessage()
        sending.SendMsg()
        # SendMsg()
        self.counter -= 1
        self.count_timer = 5
        self.num_bullet.setText(str(self.counter))
        
        self.btn_launch.setEnabled(False)
        
        # 펑 터지는 오디오
        pygame.mixer.init()
        pygame.mixer.music.load("resources/explode.mp3")
        pygame.mixer.music.play()
        
        if self.counter <= 0:
            self.console_box.append("{} 탄을 모두 소진하였습니다".format(self.ShowTimeline()))
            # self.console_box.setPlainText(self.formatted_datetime)
            # self.console_box.append("탄을 모두 소진하였습니다")
            
    def StartCountdown(self):
        """타이머 5초로 초기화하고 카운트 시작 메서드 호출"""
        self.count_timer = 5  # 초기 타이머 남은 시간
        self.UpdateCount()
        self.timer_LCD.start(1000)
            
    def UpdateCount(self):
        """LCD 타이머로 5초 카운트"""
        self.lcd_number.display(self.count_timer)
        self.count_timer -= 1

        if self.count_timer < 0:
            # 타이머 중지
            self.timer_LCD.stop()
        
            self.btn_launch.setEnabled(True)
            
    def ConsoleMsg(self):
        """콘솔 박스에 메세지 띄우기"""
        if self.msg_queue:
            msg = self.msg_queue.get()
            
            if msg == "발사 준비 완료":
                if self.counter > 0:
                    # hw 발사 준비 완료되면 카운트 시작
                    self.console_box.append("{} 발사 준비 완료 카운트 시작".format(self.ShowTimeline()))
                    if self.counter > 0:
                        self.StartCountdown()
            else:
                self.console_box.append("{} {}".format(self.ShowTimeline(), msg))
        
    def CamViewer(self):
        """웹캠 영역에 영상 띄우기"""
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
                
    def CloseThread(self, event):
        """Thread 종료"""
        self.video_thread.quit()
        self.video_thread.wait()
        self.hw_thread.quit()
        self.hw_thread.wait()
        event.accept()