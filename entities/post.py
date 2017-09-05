import uuid
from database import Database
import datetime

__author__ = 'neehad'

#create the post object
class Post(object):

    #this is the constructor
    def __init__(self, blog_id, title, content, author, created_date=datetime.datetime.utcnow(), _id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.created_date = created_date
        self._id = uuid.uuid4().hex if _id is None else _id #if the id is None then do a new one else just id

    def save_to_mongo(self):
        Database.insert(collection='posts', #name of collection is posts and data is the json data
                        data=self.json())

   #define the json object
    def json(self):
        return {
            '_id': self._id,
            'blog_id': self.blog_id,
            'author': self.author,
            'content': self.content,
            'title': self.title,
            'created_date': self.created_date
        }

    @classmethod
    def from_mongo(cls, id): #take in a post class with the id and look it up
        post_data = Database.find_one(collection='posts', query={'_id': id}) #find the entry
        return cls(**post_data)

    @staticmethod
    def from_blog(id):
        return [post for post in Database.find(collection='posts', query={'blog_id': id})]
