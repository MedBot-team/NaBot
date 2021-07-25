import sys
sys.path.insert(0, '../../chatbot')

import typing
from typing import Any, Optional, Text, Dict, List, Type

from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.components import Component

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata

from autocorrect import Speller


class SpellChecker(Component):
    @classmethod
    def required_components(cls) -> List[Type[Component]]:

        return []

    defaults = {}

    supported_language_list = ["en",
                               "pl",
                               "ru",
                               "uk",
                               "tr",
                               "es",
                               "pt",
                               "cs",
                               "el",
                               "it",
                               "fa"]


    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:

        pass

    def process(self, message: Message, **kwargs: Any) -> None:
        spell = Speller(lang='en')
        spell_med = Speller(lang='med')

        correct = spell(message.get("text"))
        med_correct = spell_med(correct)
        message.set('text', med_correct, add_to_output=True)

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:

        pass

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Text,
        model_metadata: Optional["Metadata"] = None,
        cached_component: Optional["Component"] = None,
        **kwargs: Any,
    ) -> "Component":

        if cached_component:
            return cached_component
        else:
            return cls(meta)
