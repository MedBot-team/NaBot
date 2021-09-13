import os
import sys
import random
import string
import asyncio
import unittest
from rasa.model import get_model
from rasa.nlu.test import run_evaluation
from rasa.core.test import test as core_test

path = './production/rasa-server/rasa/'
sys.path.append(path)


class TestRasaMethods(unittest.TestCase):
    model_path = './production/rasa-server/rasa/models/'
    unpacked_model = get_model(model_path)
    tmp_name = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=10))

    """
    NLU TEST
    """
    nlu_model = os.path.join(unpacked_model, "nlu")

    # Normal NLU tests data
    test_data = './development/testcase/nlu_test.yml'
    
    
    async_test_result = run_evaluation(test_data,
                                       nlu_model,
                                       successes=True,
                                       errors=True,
                                       output_directory=f'/tmp/{tmp_name}',
                                       disable_plotting=True,
                                       report_as_dict=True,
                                       )
    test_result = asyncio.run(async_test_result)

    # Test f1_score of intents
    def test_f1_intent(self):
        threshold = 1
        test_result = self.test_result
        # Check if intent extractor is in the pipeline
        if test_result['intent_evaluation'] is not None:
            # Check if multiple intent extractors are in the pipeline
            if 'report' not in test_result['intent_evaluation']:
                for intent in test_result['intent_evaluation']:
                    f1_score = test_result['intent_evaluation'][intent]['f1_score']
                    print(f1_score)
                    self.assertTrue(f1_score >= threshold)
            else:
                f1_score = test_result['intent_evaluation']['f1_score']
                print(f1_score)
                self.assertTrue(f1_score >= threshold)

    # Test f1_score of entities
    def test_f1_entity(self):
        threshold = 1
        test_result = self.test_result
        # Check if entity extractor is in the pipeline
        if test_result['entity_evaluation'] is not None:
            # Check if multiple entity extractors are in the pipeline
            if 'report' not in test_result['entity_evaluation']:
                f1_score = test_result['entity_evaluation']['RegexEntityExtractor']['f1_score']
                print(f1_score)
                self.assertTrue(f1_score >= threshold)
            else:
                f1_score = test_result['entity_evaluation']['f1_score']
                print(f1_score)
                self.assertTrue(f1_score >= threshold)


if __name__ == '__main__':
    # Run tests
    unittest.main()
