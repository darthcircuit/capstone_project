from curses import color_content
from select import select
import pwinput
import secrets
import random
import bcrypt
from date_lib import dt
from ansi_lib import *
from database import db_con, db_cur
from query_dict import to_sql

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

        email_dict = {}
        query = to_sql(query_dict)
        output_obj = db_cur.execute(query)
        results = output_obj.fetchall()

        set_font(text.bold, fg.white, text.underline)
        print(f"\n{' ':5}| {'Name':<24}| {'Email Address':<24}| {'Last Login':<14}| {'Failed Logins':<14}| {'Date Hired':<14}| {'User Type':<12}| {'Status':<10}| {'User ID':<10}")
        reset()
        
        bit_flip = 1

        for num, user in enumerate(results, start=1):
            if bit_flip == 0:
                color = set_font(bg.cyan)
                bit_flip = 1
            else:
                color = set_font(bg.blue)
                bit_flip = 0

            email_dict[str(num)] = user[2]            
            user = [str(x) for x in user]

            color 
            print(f"{num:5}| {(user[1]+', '+user[0]):<24}| {user[2]:<24}| {'Never' if not user[3] else user[3]:>14}| {'0' if not user[4] else user[4]:>14}| {user[5]:>14}| {'Manager' if user[6] == '1' else 'Employee':<12}| {'Active' if user[7] == '1' else 'Inactive':<10}| {user[8]:>10}",end="")
            reset()
            print()

        if  'select' in params:
            user_input = input("\nWhich user are you interested in? ")
            print ('\n\n')
            return email_dict[user_input]

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

            new_value = input(f'Please enter a new value for {options_dict[choice]}: ')

        else:
            print('If you would like to change your password, please enter your new one below.')
            choice = 'password'
            new_value = input('Password: ')
            options_dict[choice] = new_value
    
        query_dict = {

            'query_type': 'update',
            'field': f'{options_dict[choice]}',
            'where': {

                'field': 'user_id',
                'value': f'{selected_user.user_id}',
                'operator': 'equalto'
            }

        }
        query = to_sql(query_dict)
        print(query)
        db_cur(query)
        db_con.commit()

    def delete(email):
        user_to_del = User.select(email)
