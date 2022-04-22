from shutil import move
import pwinput
import bcrypt
from libs import *
from database import *
from reports import *

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
                
                #start main program as user:
                main_menu(User.active_user)

                print('You have been logged out.')
                continue

            else:
                db_cur.execute(f'UPDATE Users SET failed_logins = (failed_logins + 1) WHERE email = ?', (email,))
                db_con.commit()
                print("Incorrect. Please try again.")

def main_menu(logged_user):
    user_name = f'{logged_user.first_name} {logged_user.last_name}'
    last_logged = logged_user.last_login
    failed = logged_user.failed_logins
    manager = logged_user.user_type

    #reset password counter and update login time
    db_cur.execute(f'UPDATE Users SET last_login = ?, failed_logins = 0 WHERE email = ?', (dt.today, logged_user.email))
    db_con.commit()
    clear()

    
    print(f'Welcome back {user_name}!')
    print(f'You last logged in on {last_logged}')
    
    if int(failed) > 0:
        move_cursor(25,'r')
        print(f'\n\n!!WARNING!!\n')
        
        move_cursor(25,'r')
        print('- There were {failed} failed login attempts to your account since your last successful Login!\n\n')

    while True:    
        user_menu = ['Change your password', 'View your assessment results and passed competencies','Log Out']
        if int(manager) == 1:
            print(f'You are logged in with Admin Privelages. Please be careful as you edit data.\n\n')

            manager_menu = ['Change your password', 'Change another User\'s Password', 'View Users, Competencies, Assessments and Assessment Result Reports', 'Add Users or Competencies/Assessments', 'Edit User Information, Competencies, and Assessments', 'Delete an Assessment Result', 'View your assessment results and passed competencies', 'Log Out']
            table_menu = ['Users', 'Competencies', 'Assessments', 'Results']
            valid_choices = []
            for num,option in enumerate(manager_menu, start = 1):
                move_cursor(6,'r')
                valid_choices.append(num)
                print(f'[{num}]: {option}')

            choice = int(input('\n\nPlease select an option: '))

            if choice not in valid_choices:
                clear()
                move_cursor(15,'r')

                print('That was not a valid choice. Please try again.\n\n\n\n')

            elif choice == 1:

                clear()
                move_cursor(15,'r')
                print(f':Change your password:')

                move_cursor(15,'r')
                new_pw = pwinput.pwinput(prompt="Please insert your new desired password: ", mask ='*')

                User.chpw(active_user, new_pw)

                move_cursor(15,'r')                
                input("Logging your out for security purposes. Please log in again with your new password. Press Enter to continue.")
                return None

            elif choice == 2:
                clear()
                move_cursor(15,'r')
                print(f':Select a User to change the password for someone else:')
                selected_user = User.select()

                move_cursor(15,'r')
                new_pw = pwinput.pwinput(prompt=f"Please insert new desired password for {selected_user.first_name}: ", mask ='*')

                User.chpw(selected_user, new_pw)

                move_cursor(15,'r')
                input('Please press Enter to continue')

            elif choice == 3:
                clear()
                print(f':View Users, Competencies, Assessments and Assessment Result Reports:\n\n')
                valid_sub_choice = [1,2,3,4,5]
                while True:
                    
                    for num,i in enumerate(table_menu, start = 1):
                        move_cursor(15,'r')
                        print(f'[{num}]: {i}')

                    move_cursor(15,'r')
                    print(f'[{num+1}]: Go Back')
                    
                    sub_choice = int(input('\n\nPlease Select an option: '))
                    
                    if sub_choice in valid_sub_choice:
                        if sub_choice == 1:
                            clear()
                           
                            User.view()

                        elif sub_choice == 2:
                            clear()
                            Competencies.view()
                        
                        elif sub_choice == 3:
                            clear()
                            Assess.view()
                        
                        elif sub_choice == 4:
                            clear()
                            Results.view()
                        
                        elif sub_choice == 5:
                            clear()
                            break

                    else:
                        clear()
                        move_cursor(25,'r')
                        print('Invalid Choice. Try again.')
           
            elif choice == 4:
                clear()
                print(f':Add Users, Competencies, and Assessments:\n\n')

                print('Assessments are automatically created when a competency is added.\n\n')
                valid_sub_choice = [1,2,3]

                while True:
                    move_cursor(15,'r')
                    print(f'[1]: Add User')

                    move_cursor(15,'r')
                    print(f'[2]: Add Competency')

                    move_cursor(15,'r')
                    print(f'[3]: Go Back')


                    sub_choice = int(input('\n\nPlease Select an option: '))
                    
                    if sub_choice in valid_sub_choice:
                        if sub_choice == 1:
                            User.create()

                        elif sub_choice == 2:
                            Competencies.create()
                            Competencies.view()
                            print('\n\n Competency and associated Assessments created successfully.')
                            input('\nPress Enter to continue.')

                        elif sub_choice == 3:
                            break

                    else:
                        clear()
                        print("Invalid Choice. Please Try again. \n\n")

            elif choice == 5:
                clear()
                print(f':Edit User Information, Competencies, and Assessments:')

                print('Assessments are automatically updated when a competency is edited.\n\n')
                valid_sub_choice = [1,2,3]

                while True:
                    move_cursor(15,'r')
                    print(f'[1]: Edit User')

                    move_cursor(15,'r')
                    print(f'[2]: Edit Competency')

                    move_cursor(15,'r')
                    print(f'[3]: Go Back')


                    sub_choice = int(input('\n\nPlease Select an option: '))
                    
                    if sub_choice in valid_sub_choice:
                        if sub_choice == 1:
                            selected_user = User.select()
                            User.edit(active_user, selected_user)

                        elif sub_choice == 2:
                            Competencies.edit()
                            Competencies.view()
                            print('\n\n Competency and associated Assessments updated successfully.')
                            input('\nPress Enter to continue.')

                        elif sub_choice == 3:
                            break

                    else:
                        clear()
                        print("Invalid Choice. Please Try again. \n\n")

            
            elif choice == 6:
                clear()
                print(f':Delete an Assessment Result:')

            elif choice == 7:
                clear()
                print(f':View your Competency Progress:')

            elif choice == 8:
                clear()
                print(f'Logging you out. Goodbye {user_name}')
                return None

        else:
            for num,option in enumerate(user_menu):
                print(f'[{num}]: {option}')

active_user = User.select('john.i@infoxen.com')
main_menu(active_user)