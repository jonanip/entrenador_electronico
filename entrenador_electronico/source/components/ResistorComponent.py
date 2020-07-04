from .BaseComponent import BaseComponent
from entrenador_electronico.source.utils import get_content_path


class ResistorComponent(BaseComponent):
    def __init__(self):
        super(BaseComponent).__init__()
        self.name = "Resistor"
        self.icon_route = get_content_path() / "icons/resistor.png"

