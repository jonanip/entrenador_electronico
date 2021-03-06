import sys
import pathlib
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QToolBar, QAction, QStatusBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # self.windowTitleChanged.connect(self.onWindowTitleChange)

        # self.windowTitleChanged.connect(lambda x: self.my_custom_fn(x, 25))
        content_pathlib = pathlib.Path("G:\My Drive\dev\entrenador_electronico\entrenador_electronico\content")
        self.setWindowTitle("My first app")
        label = QLabel("This is a PyQt5 window!")
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)

        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)
        button_action = QAction(QIcon(str(content_pathlib.joinpath("icons/balloon-box.png"))), "my button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.on_toolbar_click)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        self.setStatusBar(QStatusBar(self))


    def on_toolbar_click(self, s):
        print("click", s)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()