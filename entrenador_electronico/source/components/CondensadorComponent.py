from entrenador_electronico.source.utils import get_content_path
from .BaseComponent import BaseComponent
from entrenador_electronico.config import config

class CondensadorComponent(BaseComponent):
    counter = 0
    def __init__(self, value=config.component_dict.condensador.default_value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = config.component_dict.condensador.default_name
        self.icon_route = get_content_path() / "icons/condensador.png"
        self.id = CondensadorComponent.counter
        self.value = value
        self.unit = config.component_dict.condensador.default_unit
        self.short_name = config.component_dict.condensador.default_shortname
        if self.drop_event:
            CondensadorComponent.counter += 1
