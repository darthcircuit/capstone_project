from select import select
import pwinput
import secrets
import random
import bcrypt
from date_lib import dt
from ansi_lib import *
from database import db_con, db_cur

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
        clear()
        print('Please enter the following info:')
        print('--------------------------------')


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
                print('Date Created: ')
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
        
        clear()
        print(f"This user's email address is:\n")
        
        set_font(text.bold, fg.white, text.underline)
        print(f"{user_dict['email']}")
        reset()
        
        print(f"\n\nPassword has been set to:\n")
        
        set_font(text.bold, fg.white, text.underline)
        print(f"{passwd.decode()}")
        reset()
        
        print(f'\nPlease share this information with the user. They will need it to login.\nThey will be able to change their password later.')
        
        created_attrs = [user_dict['first_name'],user_dict['last_name'],user_dict['email'],user_dict['password'],user_dict['date_created'],user_dict['date_hired'],user_dict['user_type']]

        db_cur.execute('INSERT INTO Users (first_name,last_name,email,password,date_created,date_hired,user_type) VALUES (?,?,?,?,?,?,?)', created_attrs)
        db_con.commit()
        
        
        return User.select(user_dict['email'])

    def select(email_address,to_print = False):
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

        return User(row_as_dict)

    def edit(self):
        pass

    def delete(email):
        user_to_del = User.select(email)

        