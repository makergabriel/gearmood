import pymongo
import datetime
import json

#TODO move this to property
gmbclient = pymongo.MongoClient("mongodb://localhost:27017/")

gmbdb = gmbclient["gearmoodbot"]
shakedownreqcoll = gmbdb["shakedownreq"]
candidatesentencecoll = gmbdb["Sentence"]

def checkgmbdb():
	print(gmbclient.list_database_names())
	dblist = gmbclient.list_database_names()
	if "gearmoodbot" in dblist:
	 	print("gearmoodbot database exists.")

	print(gmbdb.list_collection_names())
	collist = gmbdb.list_collection_names()
	if "shakedownreq" in collist:
		print("shakedownreq collection exists.", )
	if "Sentence" in collist:
		print("candidatesentence collection exists.", )
	
def save(shakedown_req):
	shakedown_req["date"] = datetime.datetime.utcnow()
	print(shakedown_req)

	if shakedown_req["id"] and shakedownreqcoll.find({ "id": shakedown_req["id"] }).count() > 0:
		print("found:", shakedown_req["id"])
		shakedownreqcoll.update_one({ "id": shakedown_req["id"]}, {"$set": shakedown_req})
	else:
		shakedownreqcoll.insert_one(shakedown_req)

def get_shakedown(id):
	return shakedownreqcoll.find({ "id": id })

def get_all_shakedowns():
	return shakedownreqcoll.find()

def save_candidate_sentence(candidate_sentence):
	candidate_sentence["date"] = datetime.datetime.utcnow()
	if "id" in candidate_sentence and candidatesentencecoll.find({ "id": candidate_sentence["id"] }).count() > 0:
		print("found:", candidate_sentence["id"])
		candidatesentencecoll.update_one({ "id": candidate_sentence["id"]}, {"$set": candidate_sentence})
	else:
		candidatesentencecoll.insert_one(candidate_sentence)
