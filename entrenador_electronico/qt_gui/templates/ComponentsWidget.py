from PyQt5 import QtGui, QtWidgets, QtCore
import pathlib
from entrenador_electronico.source.components import ResistorComponent


class Resistor():
    def __init__(self):
        self.name = "Resistor"


class ThumbListWidget(QtWidgets.QListWidget):
    def __init__(self, type, parent=None):
        super(ThumbListWidget, self).__init__(parent)
        self.setIconSize(QtCore.QSize(124, 124))
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super(ThumbListWidget, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            super(ThumbListWidget, self).dragMoveEvent(event)

    def dropEvent(self, event):
        print ('dropEvent', event)
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(QtCore.PYQT_SIGNAL("dropped"), links)
        else:
            event.setDropAction(QtCore.Qt.MoveAction)
            super(ThumbListWidget, self).dropEvent(event)


class ComponentsWidget(QtWidgets.QListWidget):
    components_dict = {
        "Resistor": pathlib.Path(
            "G:/My Drive/dev/entrenador_electronico/entrenador_electronico/qt_gui/content/icons/resistor.png")
    }
    def __init__(self, parent=None):
        super(ComponentsWidget, self).__init__(parent)
        self.ui_init()
        self.setIconSize(QtCore.QSize(124, 124))
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)


    def ui_init(self):
        self.setMaximumSize(200, 3000)
        self.setMinimumSize(100, 200)
        self.set_up_components()

    def mouseMoveEvent(self, e):
        if e.buttons() != QtCore.Qt.LeftButton:
            return

        mimeData = QtCore.QMimeData()
        mimeData.setText(self.currentItem().text())

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(QtCore.Qt.MoveAction)

    def set_up_components(self):
        for component in self.components_dict:
            print(str(self.components_dict[component]))
            item = QtWidgets.QListWidgetItem(component)
            item.setIcon(QtGui.QIcon(str(self.components_dict[component])))
            print(ResistorComponent())
            item.setData(QtCore.Qt.UserRole, ResistorComponent())
            print(item.data(QtCore.Qt.UserRole))
            self.addItem(item)
