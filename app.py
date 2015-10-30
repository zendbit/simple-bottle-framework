# import bottle framework
from baseApp import BaseApp
import os

# main class of framework
class App(BaseApp):

    # call parent init
    def __init__(self):
        BaseApp.__init__(self)

    # override set configuration
    # use custom configuration
    def set_configuration(self):
        # no need this if using uwsgi --------
        self.config['ip_address'] = '127.0.0.1'
        self.config['port'] = 9000
        self.config['reloader'] = True
        self.config['interval'] = 1
        # no uwsgi --------

        # use uwsgi server instean of default bottle framework web server
        self.config['use_uwsgi'] = True # use uwsgi webserver
        
        # default application page to show
        self.config['page_url'] = '/p/home/page/front'
        
        # web template to use
        # template can be costumize in view folder
        # you can create other template just change create and change this config
        self.config['template'] = 'default'

        # mail template and mail list configuration
        '''
        self.config['maillist'] = {
            'sikilkuinc':{
                'username':'sikilku.inc@hotmail.com',
                'password':'yourpassword',
                'sender':'sikilku.inc@hotmail.com',
                'smtp_server':'smtp-mail.outlook.com',
                'port':587}}
        '''

        # database list
        # use db_sqlite for sqlite
        # user db_postgres for postgres
        '''self.config['database'] = {'db_sqlite':{'driver':'sqlite',
            'db_list':{'custom_db_name':'path_to_sqlite_file.db'))}},
            'db_postgres':{'driver':'postgresql',
            'db_list':{'custom_db_name':{'username':'yourusername', 'port':5432, 'password':'yourpassword'}}}}

        # default database to use
        self.config['default_db_config'] = 'db_sqlite'
        '''

    # override set route
    # if you need custom route
    def set_route(self):
        pass

# use default server for development only
# if you want powerfull integrate with other webserver like apache, cherypy or other
# serve my apps
# using uwsgi
# http://projects.unbit.it/uwsgi
# default using uwsgi
application = App()

# if not using uwsgi
# use development mode
# use internal bottle framework
# if self.config['use_uwsgi'] = False will use internal bottle server
# not recomended for production purpose
if not application.config.get('use_uwsgi'):
    application.run(host=application.config['ip_address'],
        port=application.config['port'],
        reloader=application.config['reloader'],
        interval=application.config['interval'])
