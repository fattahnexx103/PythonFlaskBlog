__author__ = 'neehad'

class User(object):

    def __init__(self,email,password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def find_by_email(cls,email):
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)


    @classmethod
    def find_by_id(cls, _id):
        data = Database.find_one("users", {"id": _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email,password):
        user = User.find_by_email(email)
        if user is not None:
            #check password
            return user.password == password #check if password passed in is same as database pass
        return False



    @classmethod
    def register(cls,email,password):
        user = cls.find_by_email(email)
        if user is not None:
            #register user
            new_user = cls(email,password)
            new_user.save_to_mongo()
            session['email'] = email #stores the varaible in session
            return True
        else:
            return False


    @staticmethod
    def login(email):
        #use login_valid method to see if user is still logged in
        session['email'] = email

    @staticmethod
    def logout():
        session['email'] = None;

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def create_blog(self,title,desc):
        #author and #authorId is self generated
        blog = Blog(author = self.email,
                    _id = self._id,
                    desc = desc,
                    title = title)

        blog.save_to_mongo()

    @staticmethod
    def new_post(title,desc,date=datetime.datetime.utcnow(),blog_id):
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title = title,
                      desc = desc,
                      date = date)

    def json(self):
        return {
            "email": self.email
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())
