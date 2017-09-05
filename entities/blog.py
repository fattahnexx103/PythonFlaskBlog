import uuid
import datetime
from database import Database
from entities.post import Post

__author__ = 'neehad'


class Blog(object):
    #the __init__ is like the constructor and we set all the varaibles
    def __init__(self, author, title, author_id, description, _id=None):
        self.author = author
        self.author_id = author_id
        self.title = title
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id #we encode the id and make it random if it is null else we go with normal id

    #this makes a new post
    def new_post(self,title,content,date=datetime.datetime.utcnow()):

        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=date)
        post.save_to_mongo() #we save it to the database

    #retrieve the post from database
    def get_posts(self):
        return Post.from_blog(self._id)

    #we save the post object in the database in the collection of blogs and as json data
    def save_to_mongo(self):
        Database.insert(collection='blogs',
                        data=self.json())

    #we make json data using the variables
    def json(self):
        return {
            'author': self.author,
            'author_id': self.author_id,
            'title': self.title,
            'description': self.description,
            '_id': self._id
        }
    #getting post using id
    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find_one(collection='blogs',
                                      query={'_id': id}) #use the database methods to find it and return a blog object and set the data
        return cls(**blog_data)

    @classmethod
    def find_by_author_id(cls, author_id):
        blogs = Database.find(collection = "blogs", query={'author_id': author_id})
        #return a list of blogs
        return [cls(**blog) for blog in blogs] #return a list of block objects
