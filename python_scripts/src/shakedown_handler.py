import praw
import re
import gearmood_postgresql
import env_config
import sentence_nlp

REPLACE_NO_SPACE = re.compile(r"(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\’)|(\*)")
REPLACE_WITH_SPACE = re.compile(r"(<br\s*/><br\s*/>)|(\-)|(\[)|(\])|(\/)|(\.)|(\()|(\))|(\n)")

def preprocess_text(text):
    text = REPLACE_NO_SPACE.sub("", text.lower())
    text = REPLACE_WITH_SPACE.sub(" ", text)
    return text


class Shakedown:
	def __init__(self):
		config = env_config.EnvConfig()
		self.sentence = sentence_nlp.Sentence()
		#connect to reddit
		#this requires some setup on reddit to use the apis
		#TODO write up in README.md
		self.reddit = praw.Reddit(config.get_value("Reddit","site_name"), user_agent=config.get_value("Reddit","user_agent"))
		self.ultralight = self.reddit.subreddit(config.get_value("Reddit","subreddit"))
		self.gearmood_ps = gearmood_postgresql.GearMoodPS()
 
	#TODO extract to handler class
	#Find shakedown requests on r/ultralight using the flair
	def get_shakedown_reqs(self, req_limit, comment_limit, save_enabled):
		for submission in self.ultralight.search(query="flair:Shakedown",limit=req_limit):
			self.get_and_save_shakedown(submission, comment_limit, save_enabled)

	def get_and_save_shakedown(self, submission, comment_limit, save_enabled):
		shakedown = self.get_shakedown_data(submission, comment_limit)
		if save_enabled:
				self.gearmood_ps.save_shakedown(shakedown)
				print("Saved shakedown request {} : {}".format(shakedown["title"], "https://www.reddit.com/" + shakedown["id"]))
				self.gearmood_ps.save_sentence(shakedown["id"], shakedown["cut_sentences"])

	# Gather other data contained on the reddit posts and store in a collection for further parsing
	def get_shakedown_data(self, submission, comment_limit):
		links = re.findall("https?://[^\\s|\\]|\\)]+", submission.selftext)
		
		non_negotiable_items_clean = self.clean_non_negotiable_items(submission)
		
		# process comments
		comments_raw, comments_clean, comments_links = self.extract_comments(submission, comment_limit)

		cut_sentences = self.sentence.parse_comments(comments_raw)
		print(cut_sentences)

		shake = {
			"subreddit_id" : submission.subreddit_id,
			"id" : submission.id,
			"title" : submission.title,
			"shakedown_links" : links,
			"non_negotiable_items" : non_negotiable_items_clean,
			"selftext" : submission.selftext,
			"comments_clean" : comments_clean,
			"comments_links" : comments_links,
			"comments_raw" : comments_raw,
			"cut_sentences" : cut_sentences,
			"created_dt" : submission.created_utc
		}
		return shake

	def clean_non_negotiable_items(self, submission):
		non_negotiable_items = re.findall("non-?negotiable\\s?items?:?\\s*(.*)\n", submission.selftext.lower())
		non_negotiable_items_clean = ""
		for nni in non_negotiable_items:
				non_negotiable_items_clean += preprocess_text(nni)
		return non_negotiable_items_clean

	# TODO Preserve the comment id so it can be attached to the sentence later
	# TODO refactor to get the sentences from each comment
	# TODO get the comment update_dt to know if we already processed it
	def extract_comments(self, submission, comment_limit):
		submission.comments.replace_more(limit=comment_limit)
		comments = submission.comments.list()
		comments_clean = ""
		comments_links = []
		comments_raw = ""
		for comment in comments:
			comment_links = re.findall("https?://[^\\s|\\]|\\)]+", comment.body)
			if comment_links:
				for comment_link in comment_links:
					comments_links.append(comment_link)
					link_pattern = re.compile("(https?://[^\\s|\\]|\\)]+)")
					comment_body_no_links = link_pattern.sub("", comment.body)
			else:
				comment_body_no_links = comment.body
			comments_clean += preprocess_text(comment_body_no_links)
			comments_raw += comment.body
		return comments_raw, comments_clean, comments_links
	
	def get_shakedown_req_by_id(self, submission_id):
		submission = self.reddit.submission(id=submission_id)
		self.get_and_save_shakedown(submission, 100, True)

if __name__ == '__main__':
	shakedown = Shakedown()
	#TODO move the limits to command line arguments
	#TODO maintain starting point

	shakedown.get_shakedown_reqs(500, 100, True)
	#shakedown.get_shakedown_req_by_id("ay4ana")



