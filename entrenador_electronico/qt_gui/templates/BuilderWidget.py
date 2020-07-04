from PyQt5 import QtCore, QtGui, QtWidgets


class BuilderWidget(QtWidgets.QFrame):
    def __init__(self, *args, **kwargs):
        super(BuilderWidget, self).__init__()
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
        drop_label.setText(event.mimeData().text())
        drop_label.setGeometry(pos.x(), pos.y(), 50, 20)
        drop_label.show()
        event.acceptProposedAction()

