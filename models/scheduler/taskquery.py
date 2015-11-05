from extensions.db.connector import Connector
from extensions.db.query import Query

import time
import hashlib

class TaskQuery():
    '''
        this is task TaskQuery
        modules for scheduling system
        
        CRUD function to task.db
    '''
    
    def __init__(self, db_config):
        '''
            constructor
        '''
        self.conn = Connector(db_config)
        
    def insert(self, data):
        '''
            insert task data into task database
            all field are required
            data = {insert_fields:, insert_values:[, where:, and_where:, or_where:]}
        '''
        
        if None not in [data.get(key) for key in data]:
            conn = self.conn.connect('scheduler_db_task')
            if conn:
                cur = conn.cursor()
                
                # generate task_id
                task_id = hashlib.md5(str(time.time()).encode('UTF-8')).hexdigest()
                
                # insert task id
                data.get('insert_fields').append('task_id')
                data.get('insert_values').append(task_id)
                query = Query().generate_insert(data);
                cur.execute(query)
                conn.commit()
                conn.close()
                return {'success':{'task_id':task_id}}
            
        return {'invalid':'task_name, task_description, task_start, task_repeat fields are required'}
        
    def select(self, data):
        '''
            data is query selection
            data = {'select':'', 'join':'', where:'', and_where:'', or_where:'', limit:, offset:}
        '''
        
        conn = self.conn.connect('scheduler_db_task')
        if conn:
            cur = conn.cursor()
            query = Query().generate_select(data)
            result = self.conn.map_query_fetchall(cur.execute(query).fetchall())
            conn.commit()
            conn.close()
            return {'success':result}
            
        return {'invalid':'query syntax: ' + query}