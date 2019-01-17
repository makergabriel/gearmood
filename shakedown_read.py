#!/usr/bin/python
import praw
import re
import gearmood_mongo
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

shakedown_reqs = []

#Gather other data contained on the reddit posts and store in a collection for further parsing
def get_shakedown_data(submission, comment_limit):
	links = re.findall("https?://[^\s|\]|\)]+", submission.selftext)
	if links:
		links = links
	
	non_negotiable_items = re.findall("non-?negotiable\s?items?:?\s*(.*)\n", submission.selftext.lower())
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
		print("cooment.body: ", repr(comment.body))
		comment_links = re.findall("https?://[^\s|\]|\)]+", comment.body)
		if comment_links:
			comment_links = comment_links
			for comment_link in comment_links:
				comments_links.append(comment_link)
		link_pattern = re.compile("(https?://[^\s|\]|\)]+)")
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
def get_shakedown_reqs(req_limit, comment_limit, save_enabled):
	for submission in ultralight.search(query="flair:Shakedown",limit=req_limit):
		shake = get_shakedown_data(submission, comment_limit)
		shakedown_reqs.append(shake)
		if save_enabled:
			gearmood_mongo.save(shake)
	return shakedown_reqs

#TODO move the limits to command line arguments
get_shakedown_reqs(100, 100, True)


def get_shakdown_req_by_id(submission_id):
	submission = reddit.submission(id=submission_id)
	return get_shakedown_data(submission)

