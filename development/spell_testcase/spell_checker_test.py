################################################################
"""
Warning: This test may take a long time in the case of numerous examples
"""
################################################################

# Define Rasa spell checker path
import sys
path = '../../production/rasa-server/rasa/'
sys.path.append(path)
# Import Modules
import unittest
import nlpaug.augmenter.char as nac
from string import punctuation
from spell_checker import SpellChecker


# Path of dictionaries
dictionary_path = f"{path}dictionary/frequency_dictionary.txt"
med_dictionary_path = f"{path}dictionary/frequency_med_dictionary.txt"
bigram_path = f"{path}dictionary/frequency_bigramdictionary.txt"
med_bigram_path = f"{path}dictionary/frequency_med_bigramdictionary.txt"


# Load spell checker component of rasa
check = SpellChecker(dictionary_path, med_dictionary_path, bigram_path, med_bigram_path)
# Remove ' from punctuations
punctuation = punctuation.replace("'", "")

# Apply typo error simulation to textual input
aug = nac.KeyboardAug(
    aug_char_min=1,
    aug_char_max=4,
    aug_word_min=1,
    aug_word_max=2,
    include_special_char=False,
    include_numeric=False,
    include_upper_case=False,
)

def add_typo(word):
    return aug.augment(word)

# Read examples file line by line
def read_file():
    with open("examples.txt") as f:
        for line in f:
            line = line.strip()
            line = line.translate(str.maketrans('', '', punctuation))
            yield line

# Test how many of correct sentences remains unchanged 
class TestCorrectWords(unittest.TestCase):
    def test_spell(self):
        correct_threshold = 0.95
        corrects = [line == check.correct(line) for line in read_file()]    
        correct_percent = sum(corrects) / len(corrects)
        # print(correct_percent)
        self.assertTrue(correct_percent >= correct_threshold)

# Test how many of typo contained sentences can be corrected
class TestTypoWords(unittest.TestCase):
    def test_noise(self):
        typo_threshold = 0.4
        corrects = []
        for line in read_file():
            # Add typo 5 times, differently
            for _ in range(5):
                typo = add_typo(line)
                correction = check.correct(typo)
                corrects.append(correction == line)
                # if correction != line:
                #     print("original ==>", line)
                #     print("with typo ==> ", typo)
                #     print("after correction ==> ", correction)
        correct_percent = sum(corrects) / len(corrects)
        # print(correct_percent)
        self.assertTrue(correct_percent >= typo_threshold)

# Run unittests
if __name__ == '__main__':
    unittest.main()
