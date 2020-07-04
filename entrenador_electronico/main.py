from PyQt5.QtWidgets import QApplication
from entrenador_electronico.qt_gui.templates import MainWindow
import sys


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()


if __name__ == "__main__":
    main()