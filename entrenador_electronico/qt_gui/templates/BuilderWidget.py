from PyQt5 import QtCore, QtGui, QtWidgets
from entrenador_electronico.source.components import BaseComponent
from config import config
import importlib


class ComponentLabel(QtWidgets.QLabel):
    def __init__(self, component: BaseComponent, *args, **kwargs):
        super(ComponentLabel, self).__init__(*args, **kwargs)
        self.component = component
        self.setStatusTip(f"{self.component.name} {self.component.counter}")

    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        if event.button() == QtCore.Qt.RightButton:
            print("info")
        super(ComponentLabel, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)

            self.__mouseMovePos = globalPos

        super(ComponentLabel, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos
            if moved.manhattanLength() > 3:
                event.ignore()
                return
        super(ComponentLabel, self).mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        print("information")


class BuilderWidget(QtWidgets.QFrame):
    def __init__(self, *args, **kwargs):
        super(BuilderWidget, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setLineWidth(0.6)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event: QtGui.QDropEvent):
        if event.mimeData().text():
            pos: QtCore.QPoint = event.pos()
            component_name = event.mimeData().text()
            component_module = importlib.import_module(config.component_dict[component_name].module_path)
            component_class = getattr(component_module, config.component_dict[component_name].class_name)(drop_event=True)
            drop_component = ComponentLabel(component=component_class, parent=self)
            drop_component.setPixmap(drop_component.component.icon_qpixmap)
            drop_component.setGeometry(pos.x(), pos.y(), drop_component.width(), drop_component.height())
            drop_component.show()



    def dragMoveEvent(self, event: QtGui.QDragMoveEvent) -> None:
        pass



