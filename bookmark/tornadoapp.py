import os
from tornado import ioloop,web
from tornado.escape import json_encode,json_decode
from pymongo import MongoClient
import json
from bson import json_util
from bson.objectid import ObjectId

import sys
import datetime


MONGODB_DB_URL = os.environ.get('OPENSHIFT_MONGODB_DB_URL') if os.environ.get('OPENSHIFT_MONGODB_DB_URL') else 'mongodb://localhost:27017/'
MONGODB_DB_NAME = os.environ.get('OPENSHIFT_APP_NAME') if os.environ.get('OPENSHIFT_APP_NAME') else 'getbookmarks'

client = MongoClient(MONGODB_DB_URL)
db = client[MONGODB_DB_NAME]

class ModelNames(object):
	url = "url"
	name = "posted_by"
	text = "text"
	tags = "tags"
	title = "title"
	posted_date = "posted_date"
	likes = "likes"

	comments = "comments"
	comment_name = "comment_name"
	comment_text = "comment_text"
	comment_date = "comment_date"

class SearchBlog(web.RequestHandler,ModelNames):
	def post(self):
		data =  self.get_argument("search_text", None)
		# data = self.get_argument("search")
		story = db.stories.find({'title':{'$regex':'^'+data}})
		new = []
		for data in story:
			print type(data)
			new.append(dict(data))
		self.write(json.dumps(new, default=json_util.default))
		


class LikeHandler(web.RequestHandler,ModelNames):
	def get(self, story_id):
		story = db.stories.find_one({"_id":ObjectId(str(story_id))})
		if ModelNames.likes in story:
			update_id = db.stories.update({"_id":ObjectId(str(story_id))},{"$inc":{ModelNames.likes : 1}})
		else:
			update_id = db.stories.update({"_id":ObjectId(str(story_id))},{"$set":{ModelNames.likes : 1}})

		self.set_header("Content-Type", "application/json")
		self.set_status(201)



class IndexHandler(web.RequestHandler):
	def get(self):
		self.render("index.html")

	# def post(self):
	# 	story_data = json.loads(self.request.body)
	# 	print story_data
	# 	print ModelNames.name
	# 	sys.exit(story_data)
		
	# 	print('story created with id ' + str(story_id))
	# 	self.set_header("Content-Type", "application/json")
	# 	self.set_status(201)

class StoriesHandler(web.RequestHandler,ModelNames):
	def get(self):
		stories = db.stories.find().sort('posted_date',-1)
		self.set_header("Content-Type", "application/json")
		self.write(json.dumps(list(stories),default=json_util.default))
		

	def post(self):
		story_data = json.loads(self.request.body)
		print story_data
		print ModelNames.name
		# sys.exit(story_data)
		# story_id = db.stories.insert(story_data)
		# if story_data.has_key("1")
		if 'post_id' in story_data:
			story_id = db.stories.update({"_id":ObjectId(story_data['post_id'])},{ "$push":{ ModelNames.comments:{ModelNames.comment_name:story_data['name'],ModelNames.comment_text:story_data['comment'],ModelNames.comment_date:datetime.datetime.now()}} })
			print('Comment created with id ' + str(story_id))
			self.set_header("Content-Type", "application/json")
			self.set_status(201)
		else:
			tags = []
			for data in story_data['tag']:
				tags.append(data['tag'])
			story_id = db.stories.insert({ModelNames.name:story_data['fullname'],ModelNames.title:story_data['title'],ModelNames.url:story_data['url'],ModelNames.posted_date:datetime.datetime.now(),ModelNames.tags:tags})
			print('story created with id ' + str(story_id))
			self.set_header("Content-Type", "application/json")
			self.set_status(201)
		

class StoryHandler(web.RequestHandler):
	def get(self , story_id):
		story = db.stories.find_one({"_id":ObjectId(str(story_id))})
		self.set_header("Content-Type", "application/json")
		self.write(json.dumps((story),default=json_util.default))

	def post(self):
		story_data = json.loads(self.request.body)
		print story_data
		print ModelNames.name
		sys.exit(story_data)
		
		print('story created with id ' + str(story_id))
		self.set_header("Content-Type", "application/json")
		self.set_status(201)


settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug" : True
}

application = web.Application([
	(r'/', IndexHandler),
	(r'/index', IndexHandler),
	(r'/api/v1/stories',StoriesHandler),
	(r'/api/v1/stories/(.*)', StoryHandler),
	(r'/like/(.*)', LikeHandler),

	(r'/search', SearchBlog)
],**settings)

if __name__ == "__main__":
	application.listen(8888)
	ioloop.IOLoop.instance().start()
