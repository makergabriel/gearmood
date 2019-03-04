import praw
import re
import gearmood_postgresql
import env_config

REPLACE_NO_SPACE = re.compile(r"(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\’)|(\*)")
REPLACE_WITH_SPACE = re.compile(r"(<br\s*/><br\s*/>)|(\-)|(\[)|(\])|(\/)|(\.)|(\()|(\))|(\n)")

def preprocess_text(text):
    text = REPLACE_NO_SPACE.sub("", text.lower())
    text = REPLACE_WITH_SPACE.sub(" ", text)
    return text


class Shakedown:
	def __init__(self):
		config = env_config.EnvConfig()
		#connect to reddit
		#this requires some setup on reddit to use the apis
		#TODO write up in README.md
		self.reddit = praw.Reddit(config.get_value("Reddit","site_name"), user_agent=config.get_value("Reddit","user_agent"))
		self.ultralight = self.reddit.subreddit(config.get_value("Reddit","subreddit"))
		self.shakedown_reqs = []
		self.gearmood_ps = gearmood_postgresql.GearMoodPS()
 
	#TODO extract to handler class
	#TODO separate saving the shakedown
	#Find shakedown requests on r/ultralight using the flair
	def get_shakedown_reqs(self, req_limit, comment_limit, save_enabled):
		for submission in self.ultralight.search(query="flair:Shakedown",limit=req_limit):
			shakedown = self.get_shakedown_data(submission, comment_limit)
			self.shakedown_reqs.append(shakedown)
			if save_enabled:
				self.gearmood_ps.save_shakedown(shakedown)
				print("Saved shakedown request {} : {}".format(shakedown["title"], "https://www.reddit.com/" + shakedown["id"]))
		return self.shakedown_reqs

	#Gather other data contained on the reddit posts and store in a collection for further parsing
	def get_shakedown_data(self, submission, comment_limit):
		links = re.findall("https?://[^\\s|\\]|\\)]+", submission.selftext)
		if links:
			links = links
		
		non_negotiable_items = re.findall("non-?negotiable\\s?items?:?\\s*(.*)\n", submission.selftext.lower())
		non_negotiable_items_clean = ""
		for nni in non_negotiable_items:
			non_negotiable_items_clean += preprocess_text(nni)
		
		#process comments
		submission.comments.replace_more(limit=comment_limit)
		comments = submission.comments.list()
		comments_clean = ""
		comments_links = []
		comments_raw = ""
		for comment in comments:
			comment_links = re.findall("https?://[^\\s|\\]|\\)]+", comment.body)
			if comment_links:
				comment_links = comment_links
				for comment_link in comment_links:
					comments_links.append(comment_link)
			link_pattern = re.compile("(https?://[^\\s|\\]|\\)]+)")
			comment_body_no_links = link_pattern.sub("", comment.body)
			comments_clean += preprocess_text(comment_body_no_links)
			comments_raw += comment.body

		shake = {
			"subreddit_id" : submission.subreddit_id,
			"id" : submission.id,
			"title" : submission.title,
			"shakedown_links" : links,
			"non_negotiable_items" : non_negotiable_items_clean,
			"selftext" : submission.selftext,
			"comments_clean" : comments_clean,
			"comments_links" : comments_links,
			"comments_raw" : comments_raw
		}
		return shake
	
	def get_shakdown_req_by_id(self, submission_id):
		submission = self.reddit.submission(id=submission_id)
		return self.get_shakedown_data(submission, 100)

if __name__ == '__main__':
	shakedown = Shakedown()
	#TODO move the limits to command line arguments
	#TODO 
	shakedown.get_shakedown_reqs(25, 100, True)




