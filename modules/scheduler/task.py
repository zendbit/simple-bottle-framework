from models.scheduler.taskquery import TaskQuery

import json

class Task():
    '''
        this class is extension for handling tasking and scheduler
        suporting repeat task as scheduler
        
        this extension depend on db extension which it use sqlite
    '''
    
    def __init__(self, app):
        self.app = app
        
        # initialize connector to task database
        self.__task_query = TaskQuery(app.config.get('database').get('sqlite'))
        
    def add(self):
        data = {
            'table':'tbl_task',
            'insert_fields':[
                'task_name',
                'task_description',
                'task_start',
                'task_repeat',
                'task_type',
                'task_command'],
            'insert_values':[
                'test',
                'desc',
                '2015-05-05 22:30:33',
                3600,
                'url',
                'http://babilu.com']
        }
        
        post = self.app.req().POST
        post_data = post.get('post_data')
        
        
        return json.dumps(self.__task_query.insert(data))
        
    def select(self):
        return json.dumps(self.__task_query.select({'select':['*'], 'tables':['tbl_task']}))