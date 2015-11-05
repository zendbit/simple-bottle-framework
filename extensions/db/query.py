class Query():
    '''
        class for query builder
    '''

    def __init__(self):
        self.__query_buffer = []
    
    def __validate_fields_values(self, fields):
        '''
            validate fields value
            for validation data
            
            if type is string need to quote
            
            return string 
        '''
        
        insert_fields = []
        for field in fields:
            if type(field).__name__ != 'str':
                insert_fields.append(str(field))
            else:
                insert_fields.append('\'' + field + '\'')
                        
        return ', '.join(insert_fields)
        
    def insert(self, table):
        '''
            insert into database
        '''
        
        self.__query_buffer.append('INSERT INTO ' + table)
        return self
        
    def insert_fields(self, fields):
        '''
            fields = [field1[, field2, field3, ...]]
        '''
        
        self.__query_buffer.append('(' + ', '.join(fields) + ')')
        return self
        
    def insert_values(self, values):
        '''
            add values of insert
            must be in list or tuple
            values should be in string
            values = [1, 2, 3, \'halo\'', 5...]
        '''
        
        self.__query_buffer.append('VALUES (' + self.__validate_fields_values(values) + ')')
        return self
        
    def select(self, fields):
        '''
            add select fields
            fields = 'field1, field2, field3'
        '''
        
        self.__query_buffer.append('SELECT ' + ', '.join(fields))
        return self
        
    def from_tables(self, tables):
        '''
            add table selection with from
            tables = [tbl1[, tbl2, tbl3, ...]]
        '''
        
        self.__query_buffer.append('FROM ' + ', '.join(tables))
        return self
        
    def join(self, table, joined_field, join_type='INNER'):
        '''
            add join syntax
            table is table name = tbl
            joined_field bar.id=foo.id
            join('tbl_fobar', 'bar.id=foo.id')
            join_type is join type like INNER, OUTER, LEFT, RIGHT, LEFT OUTER, RIGHT OUTER
        '''
        
        self.__query_buffer.append(join_type + ' JOIN ' + table + ' ON ' + joined_field)
        return self
        
    def where(self, condition):
        '''
            add where condition
        '''
        
        self.__query_buffer.append('WHERE ' + condition)
        return self
        
    def and_where(self, condition):
        '''
            add and where condition
        '''
        
        self.__query_buffer.append('AND WHERE ' + condition)
        return self
        
    def or_where(self, condition):
        '''
            add or where condition
        '''
        
        self.__query_buffer.append('OR WHERE ' + condition)
        return self
        
    def limit(self, limit:50):
        '''
            add limit query
        '''
        
        self.__query_buffer.append('LIMIT ' + str(limit))
        return self
        
    def offset(self, offset:0):
        '''
            add offset query
        '''
        
        self.__query_buffer.append('OFFSET ' + str(offset))
        return self
        
    def group_by(self, groupby):
        '''
            add group by clause
        '''
        
        self.__query_buffer.append('GROUP BY ' + groupby)
        return self
        

    def order_by(self, condition):
        '''
            add order by condition
        '''
        self.__query_buffer.append('ORDER BY ' + condition)
        
    def flush(self):
        '''
            generate string query of string
            return query string and empty buffer
        '''
        
        query = ' '.join(self.__query_buffer)
        self.__query_buffer.clear()
        return query
    
    def generate_insert(self, data):
        '''
            data is insert value
            data = {table:'',
                insert_fields:[],
                insert_values:[],
                where:'',
                and_where:'',
                or_where:''}
        '''
        
        if data.get('table'):
            self.insert(data.get('table'))
            
        if data.get('insert_fields'):
            self.insert_fields(data.get('insert_fields'))
            
        if data.get('insert_values'):
            self.insert_values(data.get('insert_values'))
            
        if data.get('where'):
            self.where(data.get('where'))
            
        if data.get('and_where'):
            self.and_where(data.get('and_where'))
            
        if data.get('or_where'):
            self.or_where(data.get('or_where'))
                
        return self.flush()
        
    def generate_select(self, data):
        '''
            data is query selection
            data = {select:[],
                tables:[],
                join:[
                    {
                        table:'',
                        joined_field:'',
                        join_type:''
                    },
                    {
                        table:'',
                        joined_field:'',
                        join_type:''
                    },
                    {
                        table:'',
                        joined_field:'',
                        join_type:''
                    },
                ],
                where:'',
                and_where:'',
                or_where:'',
                group_by:'',
                order_by:'', 
                limit:, 
                offset:}
        '''
        
        if data.get('select'):
            self.select(data.get('select'))
            
        if data.get('tables'):
            self.from_tables(data.get('tables'))
            
        if data.get('join'):
            for jtbl in data.get('join'):
                self.join(jtbl.get('table'), jtbl.get('joined_field'), jtbl.get('join_type'))
                
        if data.get('where'):
            self.where(data.get('where'))
            
        if data.get('and_where'):
            self.and_where(data.get('and_where'))
            
        if data.get('or_where'):
            self.or_where(data.get('or_where'))
            
        if data.get('group_by'):
            self.group_by(data.get('group_by'))
            
        if data.get('order_by'):
            self.order_by(data.get('order_by'))
            
        if data.get('limit'):
            self.limit(data.get('limit'))
            
        if data.get('offset'):
            self.offset(data.get('offset'))
                
        return self.flush()