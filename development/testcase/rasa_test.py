import os
import random
import string
import asyncio
import unittest
from rasa.model import get_model
from rasa.nlu.test import run_evaluation


class TestRasaMethods(unittest.TestCase):
    model_path = '../../production/rasa-server/rasa/models/'
    test_data = '../../production/rasa-server/rasa/train_test_split/test_data.yml'
    test_data_typo = '../../production/rasa-server/rasa/train_test_split/test_data_typo.yml'

    unpacked_model = get_model(model_path)
    nlu_model = os.path.join(unpacked_model, "nlu")
    tmp_name = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=10))

    async_test_result = run_evaluation(test_data,
                                        nlu_model,
                                        successes=True,
                                        errors=True,
                                        output_directory=f'/tmp/{tmp_name}',
                                        disable_plotting=True,
                                        report_as_dict=True,
                                        )
    test_result = asyncio.run(async_test_result)

    async_test_result_typo = run_evaluation(test_data_typo,
                                            nlu_model,
                                            successes=True,
                                            errors=True,
                                            output_directory=f'/tmp/{tmp_name}',
                                            disable_plotting=True,
                                            report_as_dict=True,
                                            )
    test_result_typo = asyncio.run(async_test_result_typo)

    def test_f1_intent(self):
        threshold = 0.9
        test_result = self.test_result

        if test_result['intent_evaluation'] is not None:
            if 'report' not in test_result['intent_evaluation']:
                for intent in test_result['intent_evaluation']:
                    f1_score = test_result['intent_evaluation'][intent]['f1_score']
                    self.assertTrue(f1_score > threshold)
            else:
                f1_score = test_result['intent_evaluation']['f1_score']
                self.assertTrue(f1_score > threshold)

    def test_f1_entity(self):
        threshold = 0.9
        test_result = self.test_result

        if test_result['entity_evaluation'] is not None:
            if 'report' not in test_result['entity_evaluation']:
                for entity in test_result['entity_evaluation']:
                    f1_score = test_result['entity_evaluation'][entity]['f1_score']
                    self.assertTrue(f1_score > threshold)
            else:
                f1_score = test_result['entity_evaluation']['f1_score']
                self.assertTrue(f1_score > threshold)

    def test_f1_response_selector(self):
        threshold = 0.9
        test_result = self.test_result

        if test_result['response_selection_evaluation'] is not None:
            if 'report' not in test_result['response_selection_evaluation']:
                for entity in test_result['response_selection_evaluation']:
                    f1_score = test_result['response_selection_evaluation'][entity]['f1_score']
                    self.assertTrue(f1_score > threshold)
            else:
                f1_score = test_result['response_selection_evaluation']['f1_score']
                self.assertTrue(f1_score > threshold)


if __name__ == '__main__':
    unittest.main()
