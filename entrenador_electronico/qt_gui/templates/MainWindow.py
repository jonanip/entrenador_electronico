import pathlib

from PyQt5 import QtGui, QtWidgets, QtCore

from . import ComponentsWidget, BuilderWidget


class DraggableLabel(QtWidgets.QLabel):
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & QtCore.Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QtWidgets.QApplication.startDragDistance():
            return
        drag = QtGui.QDrag(self)
        mimedata = QtCore.QMimeData()
        mimedata.setText(self.text())
        drag.setMimeData(mimedata)
        pixmap = QtGui.QPixmap(self.size())
        painter = QtGui.QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction)


class DropLabel(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(DropLabel, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event: QtGui.QDropEvent):
        pos: QtCore.QPoint = event.pos()
        drop_label = QtWidgets.QLabel()
        print("label_created")
        drop_label.setText("hey")
        print("label_created")
        drop_label.setGeometry(20, 20, 50, 20)
        print("label_created")
        drop_label.show()
        print("label_created")
        event.acceptProposedAction()


class BuilderFrame(QtWidgets.QFrame):
    def __init__(self, *args, **kwargs):
        super(BuilderFrame, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setLineWidth(0.6)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            print("entered")

    def dropEvent(self, event: QtGui.QDropEvent):
        pos: QtCore.QPoint = event.pos()
        drop_label = QtWidgets.QLabel(parent=self)
        drop_label.setText("hey")
        drop_label.setGeometry(pos.x(), pos.y(), 50, 20)
        drop_label.show()
        event.acceptProposedAction()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        # self.windowTitleChanged.connect(self.onWindowTitleChange)

        # self.windowTitleChanged.connect(lambda x: self.my_custom_fn(x, 25))
        content_pathlib = pathlib.Path("G:\My Drive\dev\entrenador_electronico\entrenador_electronico\qt-gui\content")
        self.setWindowTitle("Entrenador electronico")
        self.content_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QHBoxLayout()

        self.components_widget = ComponentsWidget()
        self.main_layout.addWidget(self.components_widget, 1)

        # for i in range(12):
        #     QtWidgets.QListWidgetItem(f'item {i}', self.components_widget)

        self.builder_widget = BuilderWidget()
        self.main_layout.addWidget(self.builder_widget, 3)

        # Sets-up the toolbar
        toolbar = QtWidgets.QToolBar("My main toolbar")
        self.addToolBar(toolbar)
        button_action = QtWidgets.QAction(QtGui.QIcon(str(content_pathlib.joinpath("icons/balloon-box.png"))),
                                          "my button", self)
        button_action.setStatusTip("This is your button")
        toolbar.addAction(button_action)

        # Sets-up the statusbar
        self.setStatusBar(QtWidgets.QStatusBar(self))

        self.content_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.content_widget)
        self.show()
