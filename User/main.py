import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 750, 800)
    window.show()
    sys.exit(app.exec_())
