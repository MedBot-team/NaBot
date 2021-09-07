import typing
from typing import Any, Optional, Text, Dict, List, Type

from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.components import Component

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata

from symspellpy import SymSpell


class SpellChecker(Component):
    @classmethod
    def required_components(cls) -> List[Type[Component]]:

        return []

    defaults = {}

    supported_language_list = ["en"]


    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)

        # Path of dictionaries
        self.dictionary_path = "dictionary/frequency_dictionary.txt"
        self.med_dictionary_path = "dictionary/frequency_med_dictionary.txt"
        self.bigram_path = "dictionary/frequency_bigramdictionary.txt"
        self.med_bigram_path = "dictionary/frequency_med_bigramdictionary.txt"

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:

        pass

    def correct(self, input_term):
        # Correct english and medical typoes
        sym_spell = SymSpell(max_dictionary_edit_distance=2, 
                            prefix_length=7)

        # Load general English words
        sym_spell.load_dictionary(self.dictionary_path, term_index=0, count_index=1)
        # Load medical words
        sym_spell.load_dictionary(self.med_dictionary_path, term_index=0, count_index=1)
        # Load bigram English words
        sym_spell.load_bigram_dictionary(self.bigram_path, term_index=0, count_index=2)   
        # Load bigram medical words
        sym_spell.load_bigram_dictionary(self.med_bigram_path, term_index=0, count_index=2)        
        # Get suggestions list from SymSpell
        suggestions = sym_spell.lookup_compound(input_term,
                                        max_edit_distance=2,
                                        split_phrase_by_space=True,
                                        ignore_term_with_digits=True,
                                        ignore_non_words=True,
                                        transfer_casing=True)
        # Get the top suggestion
        first_suggestion = suggestions[0]._term
        return first_suggestion

    def process(self, message: Message, **kwargs: Any) -> None:
        # Get user message
        input_term = message.get("text")

        if len(input_term) > 3:
            # Get the top suggestion
            first_suggestion = self.correct(input_term)
            # Return top suggestion
            message.set('text', first_suggestion, add_to_output=True)
        else:
            message.set('text', input_term, add_to_output=True)

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
