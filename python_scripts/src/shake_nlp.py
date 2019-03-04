import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

import gearmood_mongo
import sys, getopt

gearmood_mongo.checkgmbdb()

#initialize sample
shakedowns = []

def usage():
	print('shake_nlp [-h] -i=<reddit_id> | -a')
	print('shake_nlp [--help] --reddit_id=<reddit_id> | --all')

try:
	opts, args = getopt.getopt(sys.argv[1:],"hi:a",["help","reddit_id=", "all"])
except getopt.GetoptError:
	print('shake_nlp [reddit_id]')
	sys.exit(2)
for opt, arg in opts:
	if opt in ("-h", "--help"):
		usage()
		#print('shake_nlp [reddit_id]')
		sys.exit()
	elif opt in ("-i", "--reddit_id"):
		shakedowns = gearmood_mongo.get_shakedown(arg)
	elif opt in ("-a", "--all"):
		print("Getting all shakedowns.")
		shakedowns = gearmood_mongo.get_all_shakedowns()
	else:
		assert False, "unhandled option"

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

def parse_candidate_text(text, sentence):
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
		

for shake in shakedowns:
	reddit_url = "https://www.reddit.com/" + shake["id"]
	print(reddit_url)
	#sent_toknenize doesn't stop at new lines/carriage returns
	#some comments use just the phrase with a punctuaion
	paragraphs = [p for p in shake["comments_raw"].split('\n') if p]
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
		#only dive into tokenized sennteces that have any of our cut words
		if any(x in text for x in cut_words):
			print("\ncandidate sentence: ", sentence)
			parsed_text = parse_candidate_text(text, sentence)
			parsed_text["reddit_url"] = reddit_url
			gearmood_mongo.save_candidate_sentence(parsed_text)
			# if len(parsed["words"]) > 1:
			# 	print("> 1 cut word: ", parsed)
			#print(parsed)

