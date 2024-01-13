import queue
import threading

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QFrame, QHBoxLayout, QTextEdit, QSizePolicy, QLCDNumber, QPushButton, QMenuBar,QStatusBar
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QCoreApplication, QUrl, QTimer, QDateTime, QRect, QSize, QMetaObject
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from receive_frame import ReceiveFrame
from receiver import ReceiveMessage
from sender import SendMsg


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 남은 탄 개수
        self.counter = 3
        self.count_timer = 5  # 초기 타이머 남은 시간
        self.initUI()
        
        # 콘솔에 출력될 시간
        current_datetime = QDateTime.currentDateTime()
        self.formatted_datetime = current_datetime.toString("yyyy-MM-dd hh:mm:ss")
        
        self.frame_queue = queue.Queue(maxsize=30)    # 프레임이 저장될 큐
        self.msg_queue = queue.Queue(maxsize=30)    # 메세지가 저장될 큐
        self.startThread()
                
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.camViewer)
        self.timer.start(30)
        
    def initUI(self):
        # UI 틀 만들기
        
        # Main window
        self.setWindowTitle('BTS')
        self.setObjectName("MainWindow")
        self.resize(800, 850)

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        # 웹캠이 들어갈 영역
        self.frame = QFrame(self.centralwidget)
        self.frame.setGeometry(QRect(60, 20, 640, 480))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")

        # 콘솔,타이머, 발사버튼, 남은 탄 갯수에 대한 그룹화 된 위젯
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QRect(60, 540, 640, 210))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        #발사 버튼?
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout") 
        
        self.console_box = QTextEdit(self.horizontalLayoutWidget)
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

        self.horizontalLayout.addWidget(self.console_box)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(60, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")

        self.lcdNumber = QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber.setMaximumSize(QSize(16777215, 70))
        self.lcdNumber.setObjectName("lcdNumber")
        self.verticalLayout.addWidget(self.lcdNumber)

        self.btn_launch = QPushButton(self.horizontalLayoutWidget)
        self.btn_launch.setEnabled(False)
        self.btn_launch.setObjectName("btn_launch")
        self.btn_launch.clicked.connect(self.btn_clicked)

        self.verticalLayout.addWidget(self.btn_launch)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.label = QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)

        self.num_bullet = QLabel(self.horizontalLayoutWidget)
        self.num_bullet.setObjectName("num_bullet")

        _translate = QCoreApplication.translate
        self.btn_launch.setText(_translate("MainWindow", "발사"))
        self.label.setText(_translate("MainWindow", "남은 탄 개수 :"))
        self.num_bullet.setText(_translate("MainWindow", str(self.counter)))

        self.horizontalLayout_2.addWidget(self.num_bullet)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.setCentralWidget(self.centralwidget)

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
        
    def startThread(self):
        self.video_thread = ReceiveFrame(self.frame_queue)
        self.video_thread.start()        
        self.hw_thread = ReceiveMessage(self.msg_queue)
        self.hw_thread.rcv_msg_signal.connect(self.console_msg)
        self.hw_thread.start()
        
    def btn_clicked(self):
        SendMsg()
        self.counter -= 1
        self.count_timer = 5
        self.num_bullet.setText(str(self.counter))
        
        # 펑 터지는 오디오
        self.media_player = QMediaPlayer()

        audio_file_path = '/home/jm/BTS/PC/Server/resources/explode.mp3'
        media_content = QMediaContent(QUrl.fromLocalFile(audio_file_path))
        self.media_player.setMedia(media_content)
        
        self.media_player.play()
        
        if self.counter == 0:
            self.console_box.append("{} 탄을 모두 소진하였습니다".format(self.formatted_datetime))
            # self.console_box.setPlainText(self.formatted_datetime)
            # self.console_box.append("탄을 모두 소진하였습니다")
            self.btn_launch.setEnabled(False)
            
    # LCD 타이머 
    def updateCount(self):
        # LCD 타이머
        timer_LCD = QTimer(self)
        timer_LCD.timeout.connect(self.updateCount)
        timer_LCD.start(1000) 
        
        if self.count_timer >= 0:
            if self.count_timer == 0:
                self.btn_launch.setEnabled(True)
            self.lcdNumber.display(self.count_timer)
            self.count_timer -= 1
        else:
            timer_LCD.stop()  # 카운트가 0 이하로 내려가면 타이머 중지
            # 버튼 활성화
            
    def console_msg(self):
        if self.msg_queue:
            msg = self.msg_queue.get()
            
            if len(msg) < 2:
                # hw 발사 준비 완료되면 카운트 시작
                self.console_box.append("{} 발사 준비 완료 카운트 시작".format(self.formatted_datetime))
                self.updateCount()
            else:
                self.console_box.append("{} {}".format(self.formatted_datetime, msg))
        
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
        self.hw_thread.quit()
        self.hw_thread.wait()
        event.accept()