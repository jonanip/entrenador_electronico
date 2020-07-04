import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.windowTitleChanged.connect(lambda x: self.my_custom_fn(x, 3))

        self.setWindowTitle("My first app")
        label = QLabel("This is a PyQt5 window!")
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)

    def onWindowTitleChange(self, s):
        print(s)

    def my_custom_fn(self, a="hey!!", b=5):
        print(a, b)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec_()