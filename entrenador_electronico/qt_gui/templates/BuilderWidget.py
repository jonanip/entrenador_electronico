import importlib

from PyQt5 import QtCore, QtGui, QtWidgets

from config import config
from entrenador_electronico.source.components import BaseComponent


class ParametersDialog(QtWidgets.QDialog):
    def __init__(self, component: BaseComponent, parent=None, *args, **kwargs):
        self.component = component
        super(ParametersDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle(f"{self.component.name} {self.component.id + 1}")
        QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        # Creates an horizontal layout for the parameters
        self.h_layout = QtWidgets.QHBoxLayout()
        # Creates a text label
        self.value_label = QtWidgets.QLabel(self.component.short_name)
        self.value_label.setAlignment(QtCore.Qt.AlignRight)
        # Creates a double value spinner
        self.value_textbox = QtWidgets.QDoubleSpinBox()
        self.value_textbox.setMaximum(1E8)
        self.value_textbox.setMinimum(-1E8)
        self.value_textbox.setValue(self.component.component_value)

        self.h_layout.addWidget(self.value_label)
        self.h_layout.addWidget(self.value_textbox)
        self.layout.addLayout(self.h_layout)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        self.component.value = self.value_textbox.value()
        self.close()



class ComponentLabel(QtWidgets.QLabel):
    def __init__(self, component: BaseComponent, event_pos=None, *args, **kwargs):
        super(ComponentLabel, self).__init__(*args, **kwargs)
        self.component = component
        self.icon = self.component.icon_qpixmap
        self.setStatusTip(self.component.status_value)
        self.create_icon()
        self.create_info_label()
        self.correct_size(event_pos=event_pos)
        self.create_connection_buttons()



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

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        print(f"{self.component.name} {self.component.id}")
        parameters_dialog = ParametersDialog(component=self.component)
        parameters_dialog.exec_()
        self.component.value = parameters_dialog.component.value
        self.update_component()


    def create_info_label(self):
        self.info_label = QtWidgets.QLabel(parent=self)
        self.info_label.setText(self.component.info_value)
        self.info_label.setAlignment(QtCore.Qt.AlignLeft)
        self.info_label.adjustSize()
        self.info_label.setGeometry((self.x() + self.icon.width() - self.info_label.width()) / 2.0, self.y(), self.info_label.width(), self.info_label.height())
        self.info_label.show()

    def update_component(self):
        self.info_label.setText(self.component.info_value)
        self.setStatusTip(self.component.status_value)
        self.info_label.setAlignment(QtCore.Qt.AlignCenter)
        self.info_label.adjustSize()
        # self.info_label.setGeometry(self.info_label.x() - self.info_label.width() / 2.0, self.info_label.y(),
        #                             self.info_label.width(), self.info_label.height())
        self.info_label.show()

    def create_connection_buttons(self):
        fixed_size = QtCore.QSize(10, 10)
        self.conn_a = QtWidgets.QPushButton(parent=self)
        self.conn_b = QtWidgets.QPushButton(parent=self)
        self.conn_a.setFixedSize(fixed_size)
        self.conn_b.setFixedSize(fixed_size)
        self.conn_a.show()
        self.conn_b.show()
        self.conn_a.move(-1, round(self.height() / 2.0) - 4)
        self.conn_b.move(self.width()-self.conn_b.width() + 1, round(self.height() / 2.0) - 4)

    def create_icon(self):
        self.setPixmap(self.component.icon_qpixmap)

    def correct_size(self, event_pos):
        self.setGeometry(event_pos.x() - round(self.width()/2.0),
                                   event_pos.y() - round(self.height()/2.0),
                                   self.icon.width(),
                                   self.icon.height() + self.info_label.height()*2.0)


class BuilderWidget(QtWidgets.QFrame):
    def __init__(self, *args, **kwargs):
        super(BuilderWidget, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setLineWidth(0.6)
        self.setAcceptDrops(True)
        self.setMinimumSize(300, 400)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event: QtGui.QDropEvent):
        if event.mimeData().text():
            pos: QtCore.QPoint = event.pos()
            component_name = event.mimeData().text()
            component_module = importlib.import_module(config.component_dict[component_name].module_path)
            component_class = getattr(component_module, config.component_dict[component_name].class_name)(
                drop_event=True)
            drop_component = ComponentLabel(component=component_class, event_pos=pos, parent=self)
            drop_component.show()

    def dragMoveEvent(self, event: QtGui.QDragMoveEvent) -> None:
        pass
