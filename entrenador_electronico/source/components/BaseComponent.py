from PyQt5 import QtGui

from entrenador_electronico.source.utils import get_content_path


class BaseComponent(object):
    counter = 0

    def __init__(self, drop_event=None):
        self.name = "default_name"
        self.drop_event = drop_event
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
