################################################################
"""
Warning: This test may take a long time in the case of numerous examples
"""
################################################################
from typing import Iterator, List, Tuple
import sys
import json
import unittest
from string import punctuation
# Define Rasa spell checker path
path = '../../production/rasa-server/rasa/'
sys.path.append(path)
from spell_checker import SpellChecker


dictionary_path: str = f"{path}dictionary/frequency_dictionary.txt"
med_dictionary_path: str = f"{path}dictionary/frequency_med_dictionary.txt"
bigram_path: str = f"{path}dictionary/frequency_bigramdictionary.txt"
med_bigram_path: str = f"{path}dictionary/frequency_med_bigramdictionary.txt"
test_exampels_path: str = "augmented_examples_test.json"

# Load spell checker component of rasa
check: object = SpellChecker(
    dictionary_path, med_dictionary_path, bigram_path, med_bigram_path)
# Remove ' from punctuations
punctuation = punctuation.replace("'", "")


def read_examples(file_path: str) -> Iterator[Tuple[str, List[str]]]:
    """Read examples json file that read line by line a json 
    file include a dict with a correct text and five typo examples
    Parameters
    ----------
    file_path : str
        address of json file
    Yields
    -------
    Iterator[Tuple[str, List[str]]]
        yields correct text and a list of five typo texts
    """
    with open(file_path) as f:
        inp: list = json.load(f)
        for texts_noises in inp:
            text: str = next(iter(texts_noises.keys()))
            noises: List[str] = next(iter(texts_noises.values()))
            text = text.strip()
            text = text.translate(str.maketrans('', '', punctuation))

            yield text, noises


class TestCorrectWords(unittest.TestCase):
    def test_spell(self):
        """Test how percent of correct sentences remains unchanged
        """
        correct_threshold: float = 0.95
        corrects: List[bool] = [t == check.correct(t) for t, _ in
                                read_examples(test_exampels_path)]
        correct_percent: float = sum(corrects) / len(corrects)

        self.assertTrue(correct_percent >= correct_threshold)


class TestTypoWords(unittest.TestCase):
    def test_noise(self):
        """Test how many of typo contained sentences can be corrected
        """
        typo_threshold: float = 0.4
        corrects: List[bool] = []
        for t, n in read_examples(test_exampels_path):
            # Add typo 5 times, differently
            corrects.extend([t == check.correct(typo) for typo in n])
        correct_percent: float = sum(corrects) / len(corrects)

        self.assertTrue(correct_percent >= typo_threshold)


if __name__ == '__main__':
    unittest.main()
