import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

# TODO move cut words to config
CUT_WORDS = (
    "drop",
    "cut",
    "leave",
    "lose",
    "trim",
    "shed",
    "cast",
    "unload",
    "strike",
    "skip",
    "throw",
    "shake",
    "shave",
    "ditch",
)
# phrases to include
# shave some weight

# phrases to ignore
# leave no trace

# A verb could be categorized to any of the following codes
VERB_CODES = {
    "VB",  # Verb, base form
    "VBD",  # Verb, past tense
    "VBG",  # Verb, gerund or present participle
    "VBN",  # Verb, past participle
    "VBP",  # Verb, non-3rd person singular present
    "VBZ",  # Verb, 3rd person singular present
}


class Sentence:
    def __init__(self):
        self.cut_words = CUT_WORDS
        #config = env_config.EnvConfig()

    def parse_candidate_text(self, text):
        parsed_text = {}
        cut_word_objs = []
        # take a closer look at which cut word is used in the sentence and how it's used
        for cut_word in self.cut_words:
            if cut_word in text:
                # check if the cut_word is used as a verb
                result = nltk.pos_tag(text)
                cut_word_obj = {
                    "value": cut_word,
                    "pos_tag": [word_obj[1] for word_obj in result if word_obj[0] == cut_word],
                }
                cut_word_objs.append(cut_word_obj)
        parsed_text["words"] = cut_word_objs
        return parsed_text

    # refactor to attach the sentence to the comment id
    def parse_comments(self, text, word_list):
        # sent_toknenize doesn't stop at new lines/carriage returns
        # some comments use just the phrase with a punctuaion
        paragraphs = [p for p in text.split("\n") if p]
        sentences = []
        for paragraph in paragraphs:
            sentences.extend(sent_tokenize(paragraph))

        cut_sentences = []
        # lets look for our cut words in the tokenized senteneces
        for sentence in sentences:
            # get the words from the sentence to avoid partial matches
            tokens = word_tokenize(sentence)
            tokens = [w.lower() for w in tokens]
            # get the text from the tokenized words
            text = nltk.Text(tokens)
            # only dive into tokenized senntences that have any of our cut words
            if any(x in text for x in word_list):
                parsed_text = self.parse_candidate_text(text)
                parsed_text["sentence"] = sentence
                cut_sentences.append(parsed_text)
        return cut_sentences
