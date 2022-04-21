import secrets
import bcrypt
from datetime import date, timedelta
from random import choices
import re
from database import *
import os
from sys import stdout, stdin

#creates user object, allows add/edit/view of db table Users
class User:

    active_user = ''
    selected_user = ''
    attr_fields = ['user_id','first_name','last_name','email','password','last_login','failed_logins','date_created','date_hired','passed_comps','user_type','status']
    
    def __init__(self,attr_dict):

        for attr in User.attr_fields:
            setattr(self,attr,attr_dict[attr])

        self.attributes = [self.user_id,self.first_name,self.last_name,self.email,self.password,self.last_login,int(self.failed_logins),self.date_created,self.date_hired,self.passed_comps,int(self.user_type),int(self.status)]

    def create():
        user_dict = {}
        query_dict = {}
        clear()

        print('Please enter the following info:')
        print('--------------------------------')

        while True:
            for info in User.attr_fields:
                if info == 'first_name':
                    user_dict[info] = input(f'First Name: ')
                    print()
                
                elif info == 'last_name':
                    user_dict[info] = input(f'Last Name: ')
                    print('')

                elif info == 'user_type':
                    admin = input('If this user is going to be a manager, enter 1. Otherwise press enter. ')
                    if admin == '1':
                        user_dict[info] = 1
                    else:
                        user_dict[info] = 0
                
                elif info == 'date_created':
                    user_dict[info] = f'{dt.today}'

                elif info == 'date_hired':
                    print('Date Hired: \n')
                    user_dict[info] = dt.get_date()

                elif info == 'email':
                    user_dict['email'] = f"{user_dict['first_name']}.{user_dict['last_name'][0:1]}@infoxen.com".lower()
                    
                    #Add some logic later to check if unique. if not unique, we'll let the user set a username, but automatically append @infoxen.com

                elif info == 'password':
                    #this will generate a random secure password and then encrypt it.
                    salt = bcrypt.gensalt()
                    passwd = secrets.token_urlsafe(10).encode("utf-8")
                    hashed = bcrypt.hashpw(passwd, salt)
                    user_dict[info] = hashed.decode('utf-8')

                else:    
                    pass
            confirm = input('\n\nIf the above info looks correct, please press enter. Press E to try entering the information again. Press any other key to cancel.')

            if not confirm:
                break
            
            elif confirm.lower() == 'e':
                continue
            
            else:
                return None
            
        clear()
        print(f"This user's email address is:\n")
        
        set_font(text.bold, fg.white, text.underline)
        print(f"{user_dict['email']}")
        reset()
        
        print(f"\nPassword has been set to:\n")
        
        set_font(text.bold, fg.white, text.underline)
        print(f"{passwd.decode()}")
        reset()
        
        print(f'\nPlease share this information with the user. They will need it to login.\nThey will be able to change their password later.\n\n')

        query_dict['query_type'] = 'write'
        query_dict['table'] = 'Users'
        query_dict['fields'] = user_dict

        query, parameters = to_sql(query_dict)
        db_cur.execute(query, parameters)
        db_con.commit()
        
        #create a test user dictionary for table_writer
        # with open('dict_writer.txt', 'w') as dict_write:
        #     dict_write.write(f'{user_dict}')

        return User.select(user_dict['email'])

    def select(email_address = '',to_print = False):

        if not email_address:
            email_address = User.view('search', 'select')
            to_print = True

        output_obj = db_cur.execute('SELECT * FROM Users WHERE email = ?', (email_address,))
        results = output_obj.fetchall()

                #if query is empty, that ID doesn't exist
        if not results:
            return None

        for row in results:
            col_names = [tup[0] for tup in output_obj.description]
            row_values = [i for i in row]
            row_as_dict = dict(zip(col_names,row_values))

        if to_print:
            for key,value in row_as_dict.items():
                print(f'{key + "":<15}{value}')

            print('\n\n')

        return User(row_as_dict)

    def view(*params):
        attr = ['User Choice', 'First Name', 'Last Name', 'Email Address', 'Last Login,', 'Failed Logins', 'Date Hired', 'User Type', 'Status', 'User ID']
        query_dict = {
            'query_type': 'read',
            'fields': [
                'first_name', 
                'last_name', 
                'email',
                'last_login',
                'failed_logins',
                'date_hired',
                'user_type',
                'status',
                'user_id'
            ],
            'table': 'Users',

            'order_by': {
                'field': 'last_name',
                'order': ''
            },
        }

        if 'search' in params:
            search_term = input('Please Type a search term: ')

            query_dict['where'] = {'OR':''}
            query_dict['where']['OR'] = [
                {
                    'field': 'first_name',
                    'value': f"'%{search_term}%'",
                    'operator': 'LIKE'
                },
                {
                    'field': 'last_name',
                    'value': f"'%{search_term}%'",
                    'operator': 'LIKE'
                }

            ]


        if 'manager' in params:
            attr = [
                'User Choice',
                'First Name', 
                'Last Name', 
                'Email Address',
                'User Type',
                'User ID'
                ]

            query_dict = {
            'query_type': 'read',
            'fields': [
                'first_name', 
                'last_name', 
                'email',
                'user_type',
                'user_id'
                ],
            'table': 'Users',

            'where':{
                'field':'user_type',
                'value':1,
                'operator':'equalto'
                },

            'order_by': {
                'field': 'last_name',
                'order': ''
                }
            }

        email_dict = {}
        query = to_sql(query_dict)
        print(query)
        output_obj = db_cur.execute(query)
        results = output_obj.fetchall()

        result_dict = {}
        result_list = []
        choices_list = []
        counter = 1
        for result in results:
            result = list(result)
            email_dict[str(counter)] = result[2]
            choices_list.append(counter)
            result.insert(0,counter)
            counter += 1

            for n,col in enumerate(result):
                result_dict[attr[n]] = col
            
            result_list.append(result_dict.copy())
        
        table_writer(result_list, attr, 2)
                

        if  'select' in params:
            user_input = input("\nWhich user are you interested in? ")
            print ('\n\n')
            return email_dict[user_input]

        # set_font(text.bold, fg.white, text.underline)
        # print(f"\n{' ':5}| {'Name':<24}| {'Email Address':<24}| {'Last Login':<14}| {'Failed Logins':<14}| {'Date Hired':<14}| {'User Type':<12}| {'Status':<10}| {'User ID':<10}")
        # reset()
        
        # bit_flip = 1

        # for num, user in enumerate(results, start=1):
        #     if bit_flip == 0:
        #         color = set_font(bg.cyan)
        #         bit_flip = 1
        #     else:
        #         color = set_font(bg.blue)
        #         bit_flip = 0

        #     email_dict[str(num)] = user[2]            
        #     user = [str(x) for x in user]

        #     color 
        #     print(f"{num:5}| {(user[1]+', '+user[0]):<24}| {user[2]:<24}| {'Never' if not user[3] else user[3]:>14}| {'0' if not user[4] else user[4]:>14}| {user[5]:>14}| {'Manager' if user[6] == '1' else 'Employee':<12}| {'Active' if user[7] == '1' else 'Inactive':<10}| {user[8]:>10}",end="")
        #     reset()
        #     print()



        print('\n')
    
    def edit(self,selected_user = False):

        manager_edit_options = ['first_name', 'last_name', 'email', 'password', 'date_hired', 'user_type', 'status']

        if not selected_user:
            selected_user = self

        if self.user_type == 1:
            options_dict = {}
            print('Please select one of the following options, or press enter to cancel: ')
            for num, option in enumerate(manager_edit_options, start=1):
                print(f'{num}) {option}: ')
                options_dict[str(num)] = option

            while True:

                choice = input()

                if not choice:
                    return None

                elif choice in options_dict:
                    break

                else:
                    print("That is not a valid option. Please pick another, or press enter to cancel.")

            choice = options_dict[choice]
            new_value = input(f'Please enter a new value for {choice}: ')


        else:
            print('If you would like to change your password, please enter your new one below.')
            choice = 'password'
            new_value = input('Password: ')
            options_dict[choice] = new_value

        if choice == 'password':
            hashed = bcrypt.hashpw(new_value.encode(),salt=bcrypt.gensalt())
            new_value = hashed.decode()
    
        query_dict = {

            'query_type': 'update',
            'table': 'Users',
            'field': f'{choice}',
            'where': {

                'field': 'user_id',
                'value': f'{selected_user.user_id}',
                'operator': 'equalto'
            }

        }
        query = to_sql(query_dict)
        db_cur.execute(query,(new_value,))
        db_con.commit()

#creates competencies object, allows add/edit/view of db table Competencies
class Competencies:

    attr_fields = ['comp_id','name','date_created']

    def __init__(self, comp_id,name,date_created):

        self.comp_id = comp_id
        self.name = name
        self.date_created = date_created

    def create():

        name = input('Please enter a name for this competency: ')
        date_created = f'{dt.today}'
        
        query = ("INSERT INTO Competencies (name,date_created) VALUES (?,?)")
        db_cur.execute(query, (name, date_created))

        db_con.commit()

        query = (f"SELECT comp_id FROM Competencies WHERE name ='{name}'")
        comp = db_cur.execute(query).fetchone()

        comp_id = comp[0] 

        new_comp = Competencies(comp_id, name, date_created)

        Assess.create(new_comp)

        return new_comp

    def view(select=False):
        clear()
        query = ("SELECT comp_id, name, date_created FROM Competencies")

        results = db_cur.execute(query).fetchall()
        attr = Competencies.attr_fields
        result_dict = {}
        result_list = []
        choices_list = []
        header = ['Competency ID', 'Name', 'Date Created']
        
        for result in results:
            for n,col in enumerate(result):
                result_dict[attr[n]] = col
                choices_list.append(result[0])
            result_list.append(result_dict.copy())

        table_writer(result_list, header, 2)
                
        if select:
            return choices_list
           
    def edit():

        choices_list = Competencies.view(True)


        while True:
            edit_sel = input('Enter the Competency ID that you would like to edit: ')
            if edit_sel in choices_list:
                break
            else:
                print('Not a valid selection. Please try select a different option.')

        col_name = input('What would you like to name this competency? ')
        
        print("When was this competency Created?\n")
        col_date = dt.get_date()

        query = (f"UPDATE Competencies SET name = '{col_name}', date_created = '{col_date}' WHERE comp_id = '{edit_sel}'")
        # params = (col_name,col_date,edit_sel)

        db_cur.execute(query)
        db_con.commit()

        comp_object = Competencies(edit_sel,col_name,col_date)

        Assess.edit(comp_object)

#creates assessments object. automatically updates when competency created/edited. allows view of db table Assessments
class Assess:

    assess_list = ['Manager Evaluation', 'Peer Evaluation', 'Practical Skills', 'Self Evaluation']
    attr_fields = ['comp_id','name','date_created']

    def __init__(self, comp_id,name,date_created):

        self.comp_id = comp_id
        self.name = name
        self.date_created = date_created

    def create(competency):
  
        #Create Competency.create() will automatically run this code to create new assessments as comps are built.

        counter = 1

        while counter <= 4:
            assess_id = f'{competency.comp_id}.{counter}'
            assess_name = f'{competency.name} - {Assess.assess_list[counter-1]}'

            assess_db = [assess_id,competency.comp_id,assess_name,counter]
            query = "INSERT INTO Assessments (assess_id, comp_id, name, assess_type) VALUES (?,?,?,?)"
            db_cur.execute(query,assess_db)

            counter += 1
    
        db_con.commit()

    def view(select=False):

        clear()
        query = ("SELECT assess_id, name FROM Assessments")

        results = db_cur.execute(query).fetchall()
        head = ['User Choice','Assessment ID', 'Assessment Name']
        result_dict = {}
        result_list = []
        choices_list = []
        counter = 1 

        for result in results:
            result = list(result)
            result.insert(0,counter)
            for n,col in enumerate(result):
                result_dict[head[n]] = col
                choices_list.append(result[0])
            result_list.append(result_dict.copy())
            counter+=1
        
        table_writer(result_list, head, 4)

        if select:
            return choices_list

    def edit(competency):

        counter = 1

        while counter <= 4:

            assess_name = f'{competency.name} - {Assess.assess_list[counter-1]}'
            assess_id = f'{competency.comp_id}.{counter}'

            assess_db = [assess_name,assess_id]
            query = "Update Assessments SET name = ? WHERE assess_id = ?"
            db_cur.execute(query,assess_db)
            db_con.commit()
            counter += 1

#creates assessment_results object. allows add/edit/view of db table Assessment_Results    
class Results:
    
    result_attr = ['result_id','assess_id','user_id','assess_date','manager_id','score']

    def __init__(self,attr_dict):

        for attr in Results.result_attr:
            setattr(self,attr,attr_dict[attr])

        self.attr = [self.result_id, self.assess_id, self.user_id, self.assess_date, self.manager_id, self.score]

    def add_result():
        result_dict = {}
        
        print("Please select Which user this attempt is for: ")
        user = User.select()

        print('Please select an assesment: ')
        assess = Assess.view(True)

        print("Who manages this employee?")
        manager = User.view('manager','select')

        #as a reminder, assess_id is created based on comp_id and assess_type.
        #result_id is determined based off of assess_id, user_id, and attempt number
        #for a second attempt for assessment 14.2 for user 12, the result_d == 14.2.12.2
        result_dict['result_id'] = f'{assess.assess_id}.{user.user_id}.{"Insert attempt # here"}'

    def view_all_results():
        query = 'SELECT * FROM Assessment_Results'

        results = db_cur.execute(query).fetchall()

        result_dict = {}
        result_list = []
        for result in results:
            for n,col in enumerate(result):
                result_dict[Results.result_attr[col]] = result[n]
            
            result_list.append(result_dict)
        
        table_writer(result_list)


    def view(self):
        pass

    def delete(self):
        pass

    def edit(self):
        pass

operator_dict = {'equalto':'=','lessthan':'<','greaterthan':'>','lessthanorequalto':'<=','greaterthanorequalto':'>=','notequalto':'!=', 'LIKE':'LIKE'}

#sets date to correct format
class dt:
    
    today = date.today()
    
    def get_date():
            while True:

                date_input = input('Type in the date (or leave blank if unknown) using this format: YYYY-MM-DD\n')
                    
                if re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', date_input):
                    print()
                    return date_input
                
                elif not date_input:
                    return None
                else:
                    print('That format was incorrect. Please Try again.')

#creates a sql script from a dictionary
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

col_name_choices = {
    #Users
    'user_id':"User ID",
    'first_name': 'First Name',
    'last_name': 'Last Name',
    'email': 'Email Address',
    'password': 'Password',
    'last_login': 'Last Login',
    'failed_logins': 'Failed Logins',
    'date_hired': 'Date Hired',
    'passed_comps': 'Passed Competencies',
    'user_type': 'User Type',
    'status': 'Status',

    #Competencies
    'comp_id':'Competency ID',

    #Assessments
    'assess_id':'Assessment ID',
    
    #Shared
    'date_created': 'Date Created',
    'name': 'Name',

    #Results
    'result_id':'Result ID',
    'assess_date':'Assessment Date',
    'manager_id':'Manager ID',
    'score':'Score'
    
}

def is_even(number):
    if number % 2 == 0: return True
    elif number == 0: return True
    return False

def table_writer(dictionary_list,desired_header,color_scheme = 0, custom_data = False):
    color_schemes = {
        0: [bg.blue,bg.cyan],
        1: [bg.blue,bg.white],
        2: [bg.blue,bg.magenta],
        3: [bg.green,bg.blue],
        4: [bg.green,bg.white],
        5: [bg.magenta,bg.white],
        6: [bg.cyan,bg.green],
        7: [bg.cyan,bg.magenta],
        8: [bg.cyan,bg.white],
        9: [bg.green,bg.magenta]
    }

    col_width = []

    for header in desired_header:
        col_width.append(len(header))

    rows = []
    #import a list of dictionaries and unpack
    for data_dict in dictionary_list:

        #find column width and append data to row
        row = []
        for num,val in enumerate(list(data_dict.values())):

            current_width = len(str(val))
            row.append(val)
            if current_width > col_width[num]:
                col_width[num] = current_width
        rows.append(row)
            
    #print the table

    #header
    for col,data in enumerate(desired_header):
        width = col_width[col]+2
        set_font(text.bold,text.underline)
        print(f' {desired_header[col]:<{width}}|',end="")
        reset()

    print()

    row_num = 1
    for row in rows:
        if is_even(row_num):
            color = set_font(color_schemes[color_scheme][0])
        else:
            color = set_font(color_schemes[color_scheme][1])

        col_num = 0
        while col_num < len(desired_header):
            color
            width = col_width[col_num]+2
            print(f" {row[col_num]:<{width}}|",end='')
            col_num += 1
        
        reset()
        print()
        row_num += 1

    print()
    #print table


# #automagically generates table for db queries created from a list of dictionaries

'''
ansi_lib.py is a collection of classes and functions that implement many
of the ANSI Escape Code functionality for VT100 terminals. It is designed
to replace libraries such as the curses and msvcrt libraries. It is 
cross-platform compatible and less dependent on native-code libraries.

With this "module", you can control many aspects of the command-line terminal
such as color, cursor position, erasing the terminal, or parts of the terminal
and printing text to the screen at any position.

The code itself was written to be understandable for those just learning to
code and, therefore, it is not necessarily "pythonic", nor optimized for speed
or space.

Copyright 2022, Jason Fletcher and DevPipeline, LLC
'''

pref = '\033['
os.system("")

class fg: 
   black = "30"
   red = "31"
   green = "32"
   yellow = "33"
   blue = "34"
   magenta = "35"
   cyan = "36"
   white = "37"

class bg:
   black = "40"
   red = "41"
   green = "42"
   yellow = "43"
   blue = "44"
   magenta = "45"
   cyan = "46"
   white = "47"

class text:
   bold = '1'
   dim = '2'
   underline = '4'
   blink = '5'    # Doesn't seem to work on MacBook Pro
   reverse = '7'
   hidden = '8'
   # double_height_top = '#3'
   # double_height_bottom = '#4'
   # single_width = '#5'
   # double_width = '#6'

class erase:
   line_right = '0K'
   line_left = '1K'
   line = '2K'
   screen_down = '0J'
   screen_up = '1J'
   screen = '2J'

class cursor:
   up = 'A'
   down = 'B'
   right = 'C'
   left = 'D'
   home = 'H'  # Upper left of screen
   reverse_linefeed = 'I'
   hide = '?25l'
   show = '?25h' 

def rgb(r, g, b): return f'{pref}48;2;{r};{g};{b}m'

def set_font(*attrs):
   # You may have any number of parameters passed to this function
   # and those parameters will be combined into a list of attributes.
   # attrs is the list of attributes
   # Example usage: 
   #     set_font(fg.green, bg.white, text.bold)
   # attrs => [fg.green, bg.white, text.bold]
   if len(attrs) > 0:
      print_code(';'.join(attrs) + 'm')

def set_color(color):
   set_font(color=color)

'''
Hides the cursor in the terminal. 
If you call this function, make sure to call show_cursor() just prior to exiting the program. Otherwise, the cursor
will remain hidden in the terminal until restarting the terminal.
'''
def hide_cursor():
   print_code(cursor.hide)

'''
Shows the cursor in the terminal
'''
def show_cursor():
   print_code(cursor.show)

cursor_directions = { 'u':cursor.up,'d':cursor.down,'r':cursor.right,'l':cursor.left, 'up':cursor.up, 'down': cursor.down, 'right':cursor.right, 'left':cursor.left }

'''
Moves the cursor {n} lines or spaces in the {direction} specified.

n: Any number from 1 to the width or height of the screen
direction: one of 'u' | 'up' | 'd' | 'down' | 'r' | 'right' | 'l' | 'left'
'''
def move_cursor(n, direction):
   d = cursor_directions[direction.lower()]
   print_code(f'{n}{d}')

'''
Writes a {line} of text to the terminal at the current cursor location
and in a given {color}.
After printing the line, this function will reset the font attributes
to default
'''
def writeln(line, color=None):
   if color:
      set_color(color)
   stdout.write(f'{line}')
   if color: 
      reset()
   stdout.flush()

'''
Writes a {line} of text to the terminal starting at the position specified
by {row} and {col}.
'''
def addstr(row, col, line):
   goto(row, col)
   stdout.write(f'{line}')
   stdout.flush()

'''
Moves the cursor to the next line downwards
'''
def next_line():
   print_code('1E')

'''
Moves the cursor to the previous line upwards
'''
def prev_line():
   print_code('1F')

'''
Moves the cursor to the {col} specified, maintaining the current row
'''
def set_col(col):
   print_code(f'{col}G')

'''
Moves the cursor to the specified {row}, {col}. The upper left is 0,0
'''
def goto(row, col):
   print_code(f'{row};{col}H')

'''
Executes the Escape Code by printing the <ESC> prefix first, then
code passed to it.
'''
def print_code(code):
   stdout.write(f'{pref}{code}')
   stdout.flush()

'''
Deletes the line on which the cursor is located
'''
def deleteln():
   print_code(erase.line)

'''
Resets the font colors and attributes to the default
'''
def reset(): 
   print_code('0m')

'''
Clears the entire console screen
'''
def clear():
   print_code('2J')

