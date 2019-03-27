import unittest

from src.shake.sentence_nlp import Sentence

class TestSentenceNLP(unittest.TestCase):
    
    def setUp(self):
        self.sentence = Sentence()

    def test_parse_no_cut_words(self):
        parsed_text = self.sentence.parse_candidate_text([])
        assert len(parsed_text["words"]) < 1

