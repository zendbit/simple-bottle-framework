# user authentication checking
# check if user already login
# or user logout

class UserAuth():
    # constructor
    def __init__(self, app):
        self.app = app
        
        # load other extension
        self.sqlite_ext = app.load_extension('pysqlite3')
        
        # init session
        self.session = self.app.import_extension('system.session').Session(self.app)
        
    # athenticate user
    def authenticate(self, email, password):
        # create user session with user and password
        user_info = self.sqlite_ext.querylib.get_user_info_by_email_password(email, password)
        
        if user_info:
            # check session
            user_session = self.session.get_session('sikilku_user')
            
            # if session exist delete and renew
            if user_session:
                self.session.delete_session('sikilku_user')

            # cteate session
            data = {'uid':user_info['uid'], 'email':user_info['email'], 'password':user_info['password']}
            self.session.add_session('sikilku_user', data)
            
            return self.session.get_session('sikilku_user')
            
        return None
            
    # check if user login
    def is_login(self):
        # check session
        user_session = self.session.get_session('sikilku_user')
        
        # check if user valid
        # if not delete session and return false
        if user_session:
            user_info = self.sqlite_ext.querylib.get_user_info_by_email_password(user_session.get('email'), user_session.get('password'))
            if user_info:
                return True
            else:
                self.session.delete_session('sikilku_user')
        
        return False

    # logout
    # delete session
    # then redirect to login page
    def logout(self):
        self.session.delete_session('sikilku_user')
        self.app.goto_url('/p/authenticate/page/signin')
        
    # get user session info
    def get_user_session(self):
        user_data = self.session.get_session('sikilku_user')
        return user_data
