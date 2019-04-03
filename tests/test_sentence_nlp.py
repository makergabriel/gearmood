from unittest import TestCase, mock

from src.shake.sentence_nlp import Sentence

class TestSentenceNLP(TestCase):
    
    def setUp(self):
        self.sentence = Sentence()

    def test_parse_no_cut_words(self):
        parsed_text = self.sentence.parse_candidate_text([])
        assert len(parsed_text["words"]) < 1

    # @mock.patch.object(nltk, 'pos_tag', return_value=)

