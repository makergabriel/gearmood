import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import env_config

cut_words = ('drop', 'cut', 'leave', 'lose', 'trim', 'shed', 'cast', 'unload', 'strike', 'skip', 'throw', 'shake', 'shave')
#phrases to include
#shave some weight

#phrases to ignore
#leave no trace

# A verb could be categorized to any of the following codes
VERB_CODES = {
    'VB',  # Verb, base form
    'VBD',  # Verb, past tense
    'VBG',  # Verb, gerund or present participle
    'VBN',  # Verb, past participle
    'VBP',  # Verb, non-3rd person singular present
    'VBZ',  # Verb, 3rd person singular present
}


class Sentence:
    def __init__(self):
        config = env_config.EnvConfig()

    def parse_candidate_text(self, text, sentence):
        parsed_text = {
            "sentence" : sentence
        }
        cut_word_objs = []
        #take a closer look at which cut word is used in the sentence and how it's used
        for cut_word in cut_words:
            if (cut_word in text):
                #print("cut_word: ", cut_word)
                #check if the cut_word is used as a verb
                result = nltk.pos_tag(text)
                #print(result)
                cut_word_obj = {
                    "value" : cut_word,
                    "pos_tag" :[word_obj[1] for word_obj in result if word_obj[0] == cut_word]
                }
                # cut_word_verb = False
                # for word_obj in result:
                # 	if word_obj[0] == cut_word and word_obj[1] in VERB_CODES:

                # 		cut_word_verb = True
                # if not cut_word_verb:
                # 	print("cut_word doesn't appear to be used as a verb")
                cut_word_objs.append(cut_word_obj)
        parsed_text["words"] = cut_word_objs
        return parsed_text
    
    def parse_comments(self, comments_raw):
        #sent_toknenize doesn't stop at new lines/carriage returns
        #some comments use just the phrase with a punctuaion
        paragraphs = [p for p in comments_raw.split('\n') if p]
        #print(paragraphs);
        sentences = []
        for paragraph in paragraphs:
            sentences.extend(sent_tokenize(paragraph))
        
        #lets look for our cut words in the tokenized senteneces
        for sentence in sentences:
            #get the words from the sentence to avoid partial matches
            tokens = word_tokenize(sentence)
            #get the text from the tokenized words
            text = nltk.Text(tokens)
            cut_sentences = []
            #only dive into tokenized sennteces that have any of our cut words
            if any(x in text for x in cut_words):
                print("\ncandidate sentence: ", sentence)
                parsed_text = self.parse_candidate_text(text, sentence)
                cut_sentences.append(parsed_text)
                # if len(parsed["words"]) > 1:
                # 	print("> 1 cut word: ", parsed)
                #print(parsed)