from entrenador_electronico.source.utils import get_content_path


class BaseComponent(object):
    def __init__(self):
        self.name = "default_name"
        self.icon_route = get_content_path()

