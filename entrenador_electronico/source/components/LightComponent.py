from .BaseComponent import BaseComponent
from entrenador_electronico.source.utils import get_content_path


class LightComponent(BaseComponent):
    counter = 0
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Light"
        self.icon_route = get_content_path() / "icons/light.png"
        self.id = LightComponent.counter
        if self.drop_event:
            LightComponent.counter += 1




