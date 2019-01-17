#!/usr/bin/python
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet


# synonyms = [] 
# antonyms = []
# for synset_name in cut_words:
# 	for synset in wordnet.synsets(synset_name):
# 		for l in synset.lemmas(): 
# 			synonyms.append(l.name()) 
# 			if l.antonyms(): 
# 				antonyms.append(l.antonyms()[0].name()) 
# print("Synonyms: ", synonyms)
# print("Antonyms: ", antonyms)


def get_phrases_concordance(target_word, text, left_margin = 10, right_margin = 10):
	## Collect all the index or offset position of the target word
    c = nltk.ConcordanceIndex(text.tokens, key = lambda s: s.lower())
 
    ## Collect the range of the words that is within the target word by using text.tokens[start;end].
    ## The map function is use so that when the offset position - the target range < 0, it will be default to zero
    concordance_txt = ([text.tokens[list(map(lambda x: x-5 if (x-left_margin)>0 else 0,[offset]))[0]:offset+right_margin]
		for offset in c.offsets(target_word)])
                         
    ## join the sentences for each of the target phrase and return it
    return [''.join([x+' ' for x in con_sub]) for con_sub in concordance_txt]

#text.concordance(cut_word)
		# concordance_result = get_phrases_concordance(cut_word, text)
		# for concordance in concordance_result:
		# 	print(concordance)
		# text.similar(cut_word)
		# text.common_contexts(cut_word)
		#if concordance:
			#print(concordance)