import json
import hashlib
import time

from extensions.system.session import Session

class Unique():
    # init action constructor
    def __init__(self, app):
        self.__app = app
        self.__session = Session(app)
        
    # get key and generate session
    def get(self):
        post = self.__app.req().POST
        if post.get('access_type') == 'browser':
            # get shared key
            shared_key = self.__session.get_session('shared_key')
            # if shared key not available generate new one
            if not shared_key:
                # generate unique id for security code
                shared_key = hashlib.md5(str(time.time()).encode('UTF-8')).hexdigest()
                self.__session.add_session('shared_key', shared_key, 60)
            return json.dumps({'shared_key':shared_key})
        
    # validate shared key
    # compare with session
    def validate(self, shared_key):
        if shared_key == self.__session.get_session('shared_key'):
            return True
        
        # if session valid delete session
        # then return true
        self.__session.delete_session('shared_key')
        return False
        
    # validate shared key
    def validate_post_key(self):
        post = self.__app.req().POST
        shared_key = post.get('shared_key')
        return self.validate(shared_key)