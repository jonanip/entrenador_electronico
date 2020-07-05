from entrenador_electronico.source.utils import get_content_path
from .BaseComponent import BaseComponent


class ResistorComponent(BaseComponent):
    counter = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Resistor"
        self.icon_route = get_content_path() / "icons/resistor.png"
        self.id = ResistorComponent.counter
        if self.drop_event:
            ResistorComponent.counter += 1
