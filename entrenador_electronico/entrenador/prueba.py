import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLabel


def window():
    app = QApplication(sys.argv)
    widget = QWidget()

    tex_label = QLabel(widget)
    tex_label.setText("Hello World!")
    tex_label.move(110, 85)

    widget.setGeometry(50, 50, 320, 200)
    widget.setWindowTitle("probatzen")
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    window()
