from models.scheduler.taskquery import TaskQuery
from modules.token.unique import Unique

import json

class Task():
    '''
        this class is extension for handling tasking and scheduler
        suporting repeat task as scheduler
        
        this extension depend on db extension which it use sqlite
    '''
    
    def __init__(self, app):
        self.__app = app
        self.__unique = Unique(app)
        
        # initialize connector to task database
        self.__task_query = TaskQuery(app.config.get('database').get('sqlite'))
        
    def add(self):
        post = self.__app.req().POST
        
        if not self.__unique.validate(post.get('shared_key')):
            return json.dumps({'invalid':'shared key'})
        
        post_data = json.loads(post.get('post_data'))
        
        insert_fields = []
        insert_values = []
        
        for field in post_data:
            insert_fields.append(field)
            insert_values.append(post_data.get(field))
        
        data = {
            'table':'tbl_task',
            'insert_fields':insert_fields,
            'insert_values':insert_values
        }
        
        return json.dumps(self.__task_query.insert(data))
        
    def select(self):
        return json.dumps(self.__task_query.select({'select':['*'], 'tables':['tbl_task']}))