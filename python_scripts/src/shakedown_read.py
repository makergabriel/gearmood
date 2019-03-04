#!/usr/bin/python
import praw
import re
import gearmood_mongo
import gearmood_postgresql
import datetime
from objdict import ObjDict

#connect to reddit with gearmoodbot
#this requires some setup on reddit to use the apis
#TODO look into better way to separate this like the praw.ini - not shared in git currently
reddit = praw.Reddit('gearmoodbot', user_agent='gearmoodbot')

REPLACE_NO_SPACE = re.compile("(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\’)|(\*)")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\[)|(\])|(\/)|(\.)|(\()|(\))|(\n)")

def preprocess_text(text):
    text = REPLACE_NO_SPACE.sub("", text.lower())
    text = REPLACE_WITH_SPACE.sub(" ", text)
    return text

ultralight = reddit.subreddit("Ultralight")

gearmood_mongo.checkgmbdb()


class Shakedown:
	def __init__(self):
		self.shakedown_reqs = []
		self.gearmood_ps = gearmood_postgresql.GearMoodPS()
 
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
			#print("cooment.body: ", repr(comment.body))
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
		"id" : submission.id
		}
		shake["title"] = submission.title
		shake["shakedown_links"] = links
		shake["non_negotiable_items"] = non_negotiable_items_clean
		shake["selftext"] = submission.selftext
		shake["comments_clean"] = comments_clean
		shake["comments_links"] = comments_links
		shake["comments_raw"] = comments_raw
		return shake
	
	#Find shakedown requests on r/ultralight using the flair
	def get_shakedown_reqs(self, req_limit, comment_limit, save_enabled):
		for submission in ultralight.search(query="flair:Shakedown",limit=req_limit):
			shake = self.get_shakedown_data(submission, comment_limit)
			self.shakedown_reqs.append(shake)
			if save_enabled:
				#gearmood_mongo.save(shake)
				self.gearmood_ps.save_shakedown(shake)
		return self.shakedown_reqs

	def get_shakdown_req_by_id(self, submission_id):
		submission = reddit.submission(id=submission_id)
		return self.get_shakedown_data(submission, 100)

if __name__ == '__main__':
	shakedown = Shakedown()
	#TODO move the limits to command line arguments
	shakedown.get_shakedown_reqs(5, 100, True)




