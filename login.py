import pwinput
import bcrypt
from libs import *
from database import *

def login():
        clear()

        print('Welcome Stranger! Please Log in!')
        
        while True:
            email = input('Please type in your Email Address (or leave blank to quit): ')
            
            if not email:
                print('Goodbye!')
                quit()

            passwd = pwinput.pwinput(prompt = 'Please Type in your password: ', mask = '*')
            
            hashed_pass = db_cur.execute("SELECT password FROM Users WHERE email = ?", (email,)).fetchone()
            
            if not hashed_pass:
                print("Incorrect. Please try again.")
                continue
            
            hashed_pass = hashed_pass[0]

            if bcrypt.checkpw(passwd.encode('utf-8'), hashed_pass.encode('utf-8')):

                User.active_user = User.select(email)
                print('login works!')
                print(f'Welcome {User.active_user.first_name}!')
                # print('You have been logged out.')
                # continue

            else:
                print("Incorrect. Please try again.")