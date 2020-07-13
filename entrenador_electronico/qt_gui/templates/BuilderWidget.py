import importlib
import numpy as np
from typing import List
from PyQt5 import QtCore, QtGui, QtWidgets

from config import config
from entrenador_electronico.source.components import BaseComponent
from entrenador_electronico.source.components.Components import Components

class ConnectionPainter(QtGui.QPainter):
    def __init__(self, *args, **kwargs):
        super(ConnectionPainter, self).__init__(*args, **kwargs)

    def paint_connections(self):
        self.drawLine(200, 100, 250, 150)


class Connections:
    """Stores the connections present in the model"""
    counter = 0
    connecting = False
    connections = []
    connection_elements = []
    has_connections = False

    @staticmethod
    def get_connection_lines(connection, frame) -> List:
        element_1: ConnectionButton = Connections.connection_elements[connection[0]]
        element_2: ConnectionButton = Connections.connection_elements[connection[1]]
        # print(f"{element_1.mapFrom(self, element_1.pos()).x()} {element_1.mapFrom(self, element_1.pos()).y()} {element_2.mapFrom(self, element_1.pos()).x()} {element_1.mapFrom(self, element_2.pos()).y()}")
        element_1_global = element_1.mapToGlobal(element_1.rect().center())
        element_2_global = element_2.mapToGlobal(element_2.rect().center())
        # print(f"Local: {self.mapFromGlobal(element_1.mapToGlobal())}")
        # Line 1
        x_1 = frame.mapFromGlobal(element_1_global).x()
        y_1 = frame.mapFromGlobal(element_1_global).y()
        x_2 = frame.mapFromGlobal(element_2_global).x()
        y_2 = frame.mapFromGlobal(element_2_global).y()

        if element_1.side == "right" and element_2.side == "left":
            if x_2 > x_1:
                q_2 = QtCore.QPoint(x_2, y_1)
            elif x_2 <= x_1:
                q_2 = QtCore.QPoint(x_2, y_1)
        if element_1.side == "right" and element_2.side == "right":
            if x_2 > x_1:
                q_2 = QtCore.QPoint(x_2, y_1)
            elif x_2 <= x_1:
                q_2 = QtCore.QPoint(x_1, y_2)

        if element_1.side == "left" and element_2.side == "left":
            if x_2 > x_1:
                q_2 = QtCore.QPoint(x_1, y_2)
            elif x_2 <= x_1:
                q_2 = QtCore.QPoint(x_2, y_1)

        if element_1.side == "left" and element_2.side == "right":
            if x_2 > x_1:
                q_2 = QtCore.QPoint(x_1, y_2)
            elif x_2 <= x_1:
                q_2 = QtCore.QPoint(x_1, y_2)

        q_1 = QtCore.QPoint(x_1, y_1)
        q_3 = q_2
        q_4 = QtCore.QPoint(x_2, y_2)
        lines = [[q_1, q_2], [q_3, q_4]]
        return lines


class ConnectionButton(QtWidgets.QPushButton):
    counter = 0
    connecting = False
    connections = []
    connection_elements = []

    def __init__(self, side=None, parent_component: BaseComponent=None, *args, **kwargs):
        super(ConnectionButton, self).__init__(*args, **kwargs)
        self.selected = False
        self.id = Connections.counter
        self.parent_element = parent_component
        self.side = side
        Connections.connection_elements.append(self)
        Connections.counter += 1

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if not self.selected:
                self.setStyleSheet("background-color: red")
                self.selected = True
                self.pair_button.setEnabled(False)
                if not Connections.connecting:
                    Connections.connecting = True
                    Connections.connect_id = self.id
                if Connections.connecting and Connections.connect_id != self.id:
                    self.setStyleSheet("")
                    Connections.connecting = False
                    Connections.connections.append([Connections.connect_id, self.id])
                    self.pair_button.setEnabled(True)
                    self.setEnabled(True)
                    self.selected = False
                    # connections_of_id = self.find_connections_by_id()
                    for element in self.find_connected_elements():
                        element.setEnabled(True)
                        element.setStyleSheet("")
                        element.pair_button.setEnabled(True)
                        element.selected = False
                    print(Connections.connections)
                    Connections.has_connections = True
                    # BuilderWidget.update()
            else:
                self.setStyleSheet("")
                self.selected = False
                self.pair_button.setEnabled(True)
        super(ConnectionButton, self).mousePressEvent(event)

    def set_pair_button(self, pair_button):
        self.pair_button = pair_button

    def find_connections_by_id(self):
        connections = np.array(Connections.connections)
        connection_with_id = []
        for idx, connection in enumerate(connections):
            if self.id in connection:
                connection_with_id.append(idx)
        return connection_with_id

    def find_connected_elements(self):
        connection_ids = self.find_connections_by_id()
        connected_elements = []
        for connection in connection_ids:
            for id in Connections.connections[connection]:
                if id != self.id:
                    connected_element_id = id
            connected_elements.append(Connections.connection_elements[connected_element_id])
        return connected_elements

    def delete_connections(self):
        connection_ids = self.find_connections_by_id()
        for connection_id in connection_ids:
            Connections.connections.pop(connection_id)


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
        self.is_rotated = False
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
            self.hide()
            self.conn_a.delete_connections()
            self.conn_b.delete_connections()
            self.component.delete_component()
            print(Components.components)
            # Delete connections of left




        if event.button() == QtCore.Qt.MidButton:
            self.rotate()

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

    def rotate(self):
        if not self.is_rotated:
            transform = QtGui.QTransform()
            transform.rotate(90)
            self.setPixmap(self.icon.transformed(transform))
            self.setGeometry(self.x(), self.y(), self.icon.height(), self.icon.width() + 2*self.info_label.height())
            self.info_label.setGeometry((self.icon.height()-self.info_label.width()) / 2.0, 0, self.info_label.width(), self.info_label.height())
            self.conn_a.setGeometry(self.icon.height() / 2 - 4, 12, self.conn_a.width(), self.conn_a.height())
            self.conn_b.setGeometry(self.icon.height() / 2 - 4, self.height() - 18, self.conn_b.width(), self.conn_b.height())
            self.is_rotated = True
        else:
            transform = QtGui.QTransform()
            transform.rotate(0)
            self.setPixmap(self.icon.transformed(transform))
            self.setGeometry(self.x(), self.y(), self.icon.width(), self.icon.height() + self.info_label.height()*2.0)
            self.info_label.setGeometry((self.icon.width()-self.info_label.width()) / 2.0, 0, self.info_label.width(), self.info_label.height())
            self.conn_a.setGeometry(-1, self.height() / 2 - 4, self.conn_a.width(), self.conn_a.height())
            self.conn_b.setGeometry(self.width() - self.conn_b.width() + 1, self.height() / 2 - 4, self.conn_b.width(), self.conn_b.height())
            # self.conn_b.setGeometry(self.icon.height() / 2 - 4, self.height() - 18, self.conn_b.width(), self.conn_b.height())
            self.is_rotated = False

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos
            if moved.manhattanLength() > 3:
                event.ignore()
                return
        super(ComponentLabel, self).mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.buttons() == QtCore.Qt.LeftButton:
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
        self.info_label.adjustSize()
        if not self.is_rotated:
            self.info_label.setGeometry((self.icon.width() - self.info_label.width()) / 2.0, self.info_label.y(), self.info_label.width(),
                                        self.info_label.height())
        else:
            self.info_label.setGeometry((self.icon.height() - self.info_label.width()) / 2.0, self.info_label.y(),
                                        self.info_label.width(), self.info_label.height())
        self.info_label.show()

    def create_connection_buttons(self):
        fixed_size = QtCore.QSize(10, 10)
        self.conn_a = ConnectionButton(parent=self, side="left", parent_component=self.component)
        self.conn_b = ConnectionButton(parent=self, side="right", parent_component=self.component)
        self.conn_a.set_pair_button(self.conn_b)
        self.conn_b.set_pair_button(self.conn_a)

        self.conn_a.setFixedSize(fixed_size)
        self.conn_b.setFixedSize(fixed_size)
        self.conn_a.show()
        self.conn_b.show()
        self.conn_a.move(-1, round(self.height() / 2.0) - 4)
        self.conn_b.move(self.width()-self.conn_b.width() + 1, round(self.height() / 2.0) - 4)
        # if Connections.has_connections:
        #     BuilderWidget.update()
        # if Connections.connections:
        #     BuilderWidget.update()
        #     BuilderWidget.paintEvent()

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
        self.connection_painter = ConnectionPainter(self)
        self.connection_painter.setPen(QtGui.QColor(100, 100, 100))
        self.connection_painter.paint_connections()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtCore.Qt.red)
        painter.setPen(pen)
        if Connections.connections:
            for connection in Connections.connections:
                connection_lines = Connections.get_connection_lines(connection, self)
                for line in connection_lines:
                    painter.drawLine(line[0], line[1])
        self.update()

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
            # Components.component_widget[component_class.id] = drop_component
            drop_component.show()

    def dragMoveEvent(self, event: QtGui.QDragMoveEvent) -> None:
        pass
