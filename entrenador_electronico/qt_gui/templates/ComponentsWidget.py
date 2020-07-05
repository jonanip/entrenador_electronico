from PyQt5 import QtGui, QtWidgets, QtCore
import pathlib
from entrenador_electronico.source.components import ResistorComponent
from config import config
import importlib


class ComponentsWidget(QtWidgets.QListWidget):
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
        for component in config.component_dict:
            component_module = importlib.import_module(config.component_dict[component].module_path)
            component_class = getattr(component_module, config.component_dict[component].class_name)
            item = QtWidgets.QListWidgetItem(component)
            item_instance = component_class()
            item.setIcon(QtGui.QIcon(item_instance.icon_path))
            item.setData(QtCore.Qt.UserRole, item_instance)
            self.addItem(item)