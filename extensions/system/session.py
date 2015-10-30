# this class will handle sesstion control for this system
# sesstion control will implemented using pickle module
# session will be have session start date
# and session expired in a minute

import uuid
import time
import os
import pickle
import glob
import traceback

class Session():
    # constructor
    def __init__(self, app):
        self.app = app
        self.session_cache_dir = os.path.sep.join((os.getcwd(), 'extensions', 'system', 'session_cache', ''))
        self.session_secret = 'bakiak#*&@'

        # check session dir
        # if not exist create it
        if not os.path.isdir(self.session_cache_dir):
            os.mkdir(self.session_cache_dir, mode=0o775)

    # write session to file as pickle
    def serialize_session(self, session_dict, wfile):
        session_file = open(wfile, 'wb')
        pickle.dump(session_dict, session_file)
        session_file.close()
            
    # read session file from pickle
    def unserialize_session(self, rfile):
        if os.path.isfile(rfile):
            
            session_file = open(rfile, 'rb')
            session_dict = pickle.load(session_file)
            session_file.close()
            return session_dict
                
        return None

    # get session file info
    def get_session_file_info(self, session_file):
        if os.path.isfile(session_file):
            file_info = {}
            file_info['indentity'] = session_file.split(os.path.sep)[-1].split('_')[0]
            file_info['max_age'] = float(session_file.split(os.path.sep)[-1].split('_')[-1])
            return file_info
            
        return None
    
    # add session
    # session_name is session to be set
    # session_age is integer type. age in minutes. Default value is 3600 second mean 5 minutes
    # session_value is value for session name
    def add_session(self, session_name, session_value, session_age=3600):
        # init variable
        session_file = None
        identity = None
        update = False
        if self.get_session_file(session_name) and not self.is_session_expired(session_name):
            session_file = self.get_session_file(session_name)
            identity = self.get_session_file_info(session_file).get('indentity')
            update = True
        
        else:
            identity = str(uuid.uuid4())
            session_file = ''.join((self.session_cache_dir, identity, '_' , str(time.time() + session_age)))

        # create dictionary object ad serialize into unique filename
        # name should be identyty_(timecreated+max_age)
        # serialize session using pickle module
        self.app.res().set_cookie(session_name, identity, secret=self.session_secret, path='/', max_age=session_age)
        session_dict = {}
        
        if update:
            session_dict = self.unserialize_session(session_file)

        session_dict[session_name] = session_value
        self.serialize_session(session_dict, session_file)
        
    # get session cookie
    def get_sesion_cookie(self, session_name):
        return self.app.req().get_cookie(session_name, default=None, secret=self.session_secret)
    
    # get session file
    # will return session file path if exist
    # else with return None
    def get_session_file(self, session_name):
        session_cookie = self.get_sesion_cookie(session_name)
        
        # if session cookie not found return None
        if not session_cookie:
            return None
        
        session_file = glob.glob(''.join((self.session_cache_dir, session_cookie, '*')))
        
        if len(session_file):
            return session_file[0]
        
        return None
        
    
    # check if session is expired
    def is_session_expired(self, session_name):
        session_file = self.get_session_file(session_name)
        
        if session_file:
            # compare max age session file with current time in second
            if (self.get_session_file_info(session_file).get('max_age') - time.time()) <= 0:
                return True
                
        return False
                
    # get session
    # session_name is session name to get
    # will return value of session_name
    # if not exist will return None
    # if session_name equal to None, will return all session data
    def get_session(self, session_name=None):
        if self.get_session_file(session_name) and not self.is_session_expired(session_name):
            session_data = self.unserialize_session(self.get_session_file(session_name))
            
            if session_name:
                return session_data.get(session_name)
            
            else:
                return session_data
            
        return None
        
    # delete_session
    # session_name is session session name to delete
    def delete_session(self, session_name=None):
        session_file = self.get_session_file(session_name)
        
        if session_file:
            # delete session data
            if not session_name:
                os.remove(session_file)
                self.app.res().delete_cookie(session_name, path='/')
                
            # for delete specific session data
            else:
                session_dict = self.unserialize_session(session_file)
                
                if session_dict.get(session_name):
                    session_dict.pop(session_name)
                    self.serialize_session(session_dict, session_file)

    # check session file
    # should be call from thread
    def cleanup_session_file(self):
        while True:
            try:
                time.sleep(10)
                session_file = glob.glob(''.join((self.session_cache_dir, '*')))

                # limit to 500 file each iteration
                # make bullet proof from huge of file in one iteration
                if len(session_file) > 500:
                    session_file = session_file[:500]

                # cleanup file if already expired
                for sfile in session_file:
                    expired = float(sfile.split(os.path.sep)[-1].split('_')[-1])
                    expired = expired - time.time()

                    if expired < 0:
                        os.remove(sfile)

            except Exception:
                print(traceback.format_exc())
