class SQLiteConn():
    '''
        sqlite connector
    '''
    def __init__(self, connector):
        self.connector = connector
        
    def connect(self, db_name):
        
        # import sqlite
        import sqlite3
        
        conn = None
        
        try:
            # connect database
            conn = sqlite3.connect(self.connector.db_names.get(self.connector.db_config).get('db_list').get(db_name), check_same_thread=False)
            conn.row_factory = sqlite3.Row
            # register function
            for fn in self.connector.create_function:
                conn.create_function(fn.get('name'), fn.get('num_param'), fn.get('function'))
                
            cur =  conn.cursor()
            
            # set pragma
            cur.execute('PRAGMA max_page_count=2147483646;')
            cur.execute('PRAGMA page_size=65536;')
            cur.execute('PRAGMA application_id=1;')
            cur.execute('PRAGMA encoding="UTF-8";')
            cur.execute('PRAGMA recursive_triggers=true;')
            cur.execute('PRAGMA secure_delete=true;')
            cur.execute('PRAGMA synchronous=NORMAL;')
            cur.execute('PRAGMA wal_checkpoint(TRUNCATE);')
            cur.execute('PRAGMA busy_timeout=30000;')
            cur.execute('PRAGMA threads=1024;')
            cur.execute('PRAGMA main.locking_mode=NORMAL;')
            
            conn.commit()
            
        except Exception as e:
            print('error to connect database ' + str(e))
            
        return conn

class Connector():
    def __init__(self, db_names, db_config):
        '''
            constructor
        '''
        
        # init database path location
        self.db_names = db_names
        self.db_config = db_config
        
        self.create_function = []
    
    def connect(self, db_name):
        '''
            connect to database
            return cursor
        '''
        
        # check db connector driver
        # if connect to sqlite
        if self.db_names.get(self.db_config).get('driver') == 'sqlite':
            return SQLiteConn(self).connect(db_name)
            
        # if connect to postgresql
        elif self.db_names.get(self.db_config).get('driver') == 'postgresql':
            pass
            
    # string quote
    # will return text with string_quote
    # '\'text\''
    def squote(self, text):
        return '\'' + text + '\''
    
    def map_query_fetchall(self, link_data_res):
        '''
            generate mapping data
        '''
        if not link_data_res:
            return []
            
        link_data_list = []

        # generate data to dictionary
        # mapping sqlite to dict
        for link in link_data_res:
            link_data = {}
            for key in link.keys():
                link_data[key] = link[key]

            link_data_list.append(link_data)

        return link_data_list

    def map_query_fetchone(self, link_data_res):
        '''
            generate mapping data
        '''
        
        if not link_data_res:
            return {}
        
        # generate data to dictionary
        # mapping sqlite to dict
        link_data = {}
        for key in link_data_res.keys():
            link_data[key] = link_data_res[key]

        return link_data