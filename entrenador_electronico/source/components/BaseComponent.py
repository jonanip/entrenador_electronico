from entrenador_electronico.source.utils import get_content_path
from PyQt5 import QtWidgets, QtCore, QtGui

class BaseComponent(object):
    def __init__(self):
        self.name = "default_name"
        self.icon_route = get_content_path()

    @property
    def icon_path(self):
        return str(self.icon_route)

    @property
    def icon_qicon(self):
        return QtGui.QIcon(self.icon_path)

    @property
    def icon_qpixmap(self):
        return QtGui.QPixmap(self.icon_path)



