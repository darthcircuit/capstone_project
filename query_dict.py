# and_or_list = ['AND', 'OR', 'NOT']
operator_dict = {'equalto':'=','lessthan':'<','greaterthan':'>','lessthanorequalto':'<=','greaterthanorequalto':'>=','notequalto':'!=', 'LIKE':'LIKE'}

def to_sql(sql_dict):
   
   query_type = sql_dict['query_type']
   table = sql_dict['table']
   where = ''


   if 'where' in sql_dict:
      where = 'WHERE'

      
      
      if "AND" in sql_dict['where'] or "OR" in sql_dict['where'] or "NOT" in sql_dict['where']:
         count = 1
         for i in sql_dict['where']:
            for dict in sql_dict['where'][i]:
               
               field = dict['field']
               value = dict['value']
               operator = dict['operator']
            
               where = where + f' {field} {operator_dict[operator]} {value}{" " + i if count < len(sql_dict["where"][i]) else ""}'
               count += 1
      else:
         field = sql_dict['where']['field']
         value = sql_dict['where']['value']
         operator = sql_dict['where']['operator']

         where = where + f' {field} {operator_dict[operator]} {value}'

   #READ
   if query_type == 'read':
      order_by = ''
      limit = ''      
      
      if 'order_by' in sql_dict:
         order_by = f"ORDER BY {(sql_dict['order_by']['field'])} {(sql_dict['order_by']['order'])}"

      if 'limit' in sql_dict:
         limit = f"LIMIT {sql_dict['limit']}"

      columns = ', '.join(list(sql_dict['fields']))
      query = f'SELECT {columns} FROM {table} {where} {order_by} {limit}'
      return query

   #WRITE
   elif query_type == 'write':
      columns = []
      values = []
      val_var = []
      for key,val in sql_dict['fields'].items():
         if val == None:
            pass
         
         else:         
            columns.append(key)
            values.append(str(val))
            val_var.append('?')

      columns = ", ".join(columns)
      val_var = ", ".join(val_var)
      # values = ', '.join(values)

      query = f'INSERT INTO {table} ({columns}) VALUES ({val_var})'
      return query, values

   #UPDATE
   elif query_type == 'update':
      field = sql_dict['field']


      query = f'UPDATE {table} SET {field} = ? {where} '

   return query
