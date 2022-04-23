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
            
            result = db_cur.execute("SELECT password,status FROM Users WHERE email = ?", (email,)).fetchone()
            
            if not result:
                print("Incorrect. Please try again.")
                continue
            
            hashed_pass = result[0]
            status = result[1]

            if bcrypt.checkpw(passwd.encode('utf-8'), hashed_pass.encode('utf-8')):

                User.active_user = User.select(email)
                print(f'Welcome {User.active_user.first_name}!')
                
                #start main program as user:
                main_menu(User.active_user)

                clear()
                print('You have been logged out.')
                continue

            else:

                if int(status) == 0:
                    clear()
                    print('Your account has been disabled. Please speak with your manager. \n\n')
                    User.view('manager')

                else:
                    clear()
                    print("Incorrect. Please try again.")

                db_cur.execute(f'UPDATE Users SET failed_logins = (failed_logins + 1) WHERE email = ?', (email,))
                db_con.commit()

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
        move_cursor(6,'r')
        print(f'\n\n!!WARNING!!\n')
        
        move_cursor(6,'r')
        print(f'- There were {failed} failed login attempts to your account since your last successful Login!\n\n')

    while True:    
        user_menu = ['Change your password', 'View your assessment results and passed competencies','Log Out']

        #Manager Menu
        if int(manager) == 1:
            print(f'You are logged in with Admin Privelages. Please be careful as you edit data.\n\n')

            manager_menu = ['Change your password', 'Change another User\'s Password', 'View Users, Competencies, and Assessments', 'Add Users or Competencies/Assessments', 'Edit User Information, Competencies, and Assessments', 'View your Competency Progress', 'View, Add and Edit Assessment Results', 'Import and Export Reports','Log Out']
            table_menu = ['Users', 'Competencies', 'Assessments', 'Results']
            valid_choices = []
            for num,option in enumerate(manager_menu, start = 1):
                move_cursor(6,'r')
                valid_choices.append(num)
                print(f'[{num}]: {option}')

            choice = int(input('\n\nPlease select an option: '))

            if choice not in valid_choices:
                clear()
                move_cursor(6,'r')

                print('That was not a valid choice. Please try again.\n\n\n\n')


            #Change your pass
            elif choice == 1:

                clear()
                move_cursor(6,'r')
                print(f':Change your password:\n\n')

                move_cursor(6,'r')
                new_pw = pwinput.pwinput(prompt="Please insert your new desired password (or leave blank to cancel): ", mask ='*')

                if not new_pw: 
                    print('Cancelling. ')
                    continue

                User.chpw(logged_user, new_pw)

                move_cursor(6,'r')                
                input("\n\nLogging your out for security purposes. Please log in again with your new password. Press Enter to continue.")
                return None

            #Change someone else's pass
            elif choice == 2:
                clear()
                move_cursor(6,'r')
                print(f':Select a User to change the password for someone else\n\n:')
                selected_user = User.select()

                move_cursor(6,'r')
                new_pw = pwinput.pwinput(prompt=f"Please insert new desired password for {selected_user.first_name} or leave blank to cancel: ", mask ='*')

                if not new_pw:
                    clear() 
                    print('\nCancelling. ')
                    continue

                User.chpw(selected_user, new_pw)
                move_cursor(6,'r')
                input('\n\nPassword Changed Successfully. Please press Enter to continue')

            #View User,Comp,Assess
            elif choice == 3:
                clear()
                print(f':View Users, Competencies,and Assessments:\n\n')
                valid_sub_choice = [1,2,3,4]
                while True:
                    
                    for num,i in enumerate(table_menu[:3], start = 1):
                        move_cursor(6,'r')
                        print(f'[{num}]: {i}')

                    move_cursor(6,'r')
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
                            break

                    else:
                        clear()
                        move_cursor(6,'r')
                        print('Invalid Choice. Try again.')

            #Add User,Comp,Assess
            elif choice == 4:
                clear()
                print(f':Add Users, Competencies, and Assessments:\n\n')

                print('Assessments are automatically created when a competency is added.\n\n')
                valid_sub_choice = [1,2,3]

                while True:
                    move_cursor(6,'r')
                    print(f'[1]: Add User')

                    move_cursor(6,'r')
                    print(f'[2]: Add Competency')

                    move_cursor(6,'r')
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

            #Edit User,Comp, Assess
            elif choice == 5:
                clear()
                print(f':Edit User Information, Competencies, and Assessments:')

                print('Assessments are automatically updated when a competency is edited.\n\n')
                valid_sub_choice = [1,2,3]

                while True:
                    move_cursor(6,'r')
                    print(f'[1]: Edit User')

                    move_cursor(6,'r')
                    print(f'[2]: Edit Competency')

                    move_cursor(6,'r')
                    print(f'[3]: Go Back')


                    sub_choice = int(input('\n\nPlease Select an option: '))
                    
                    if sub_choice in valid_sub_choice:
                        if sub_choice == 1:
                            selected_user = User.select()
                            User.edit(logged_user, selected_user)
                            
                            #Show updated fields after updates have run:
                            clear()
                            User.select(selected_user.email,True)

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
                print(f':View your Competency Progress:')
                Results.view_user_competency(logged_user)

            #Reports Menu (View Assessment Results, Import, Export)
            elif choice == 7:
                valid_sub_choices = []
                results_table = ['View Results for an Individual','View All Results for a Competency','Enter Results for an Individual','Edit Results for an Assesment','Delete an Assessment Result','Go Back']

                while True:

                    for num,option in enumerate(results_table,start=1):
                        move_cursor(6,'r')
                        print(f'[{num}]: {option}')
                        valid_sub_choices.append(num)

                    move_cursor(6,'r')                   
                    sub_choice = int(input('\n\nPlease Select an option: '))

                    if sub_choice not in valid_sub_choices:
                        print('Invalid Option. Please Try again.')
                        continue

                    else:

                        if sub_choice == 1:
                            clear()
                            print('View Results for an Individual')

                            Results.view_user_competency(None)

                        if sub_choice == 2:
                            clear()
                            print('View All Results for a Competency')

                            Results.view_comp()

                        if sub_choice == 3:
                            clear()
                            print('Enter Results for an Individual')
                            user = User.select()
                            Results.add_result(user)

                        if sub_choice == 4:
                            clear()
                            print('Edit Results for an Assesment')

                            Results.edit()


                        if sub_choice == 5:
                            print('Delete an Assessment Result')

                            Results.delete()

                        if sub_choice == 6:
                            print('Go Back')
                            break
            
            #delete Assessment Result
            elif choice == 8:
                clear()
                print(f':Import and Export Reports:')

                valid_sub_choices = []
                reports_table = ['Export Individual User Assessment Report to CSV','Export Competency Assessment Report to CSV','Import CSV with Assessment Result information','Generate template for importing scores from CSV','Go Back']

                while True:

                    for num,option in enumerate(reports_table,start =1):
                        move_cursor(6,'r')
                        print(f'[{num}]: {option}')
                        valid_sub_choices.append(num)

                    move_cursor(6,'r') 
                    sub_choice = int(input('\n\nPlease Select an option: '))

                    if sub_choice not in valid_sub_choices:
                        print('Invalid Option. Please Try again.')
                        continue

                    else:

                        if sub_choice == 1:
                            print('Export Individual User Assessment Report to CSV')

                            Reports.export_csv(1)

                        if sub_choice == 2:
                            print('Export Competency Assessment Report to CSV')

                            Reports.export_csv(2)

                        if sub_choice == 3:
                            print('Import CSV with Assessment Result information')

                            Reports.import_csv()

                        if sub_choice == 4:
                            print('Generate template for importing scores from CSV')

                            Reports.gen_template()

                        if sub_choice == 5:
                            print('Go Back')
                            break
            
            #Log Out
            elif choice == 9:
                clear()
                print(f'Logging you out. Goodbye {user_name}')
                return None
        
        #User Menu
        else:
            valid_choices = []
            while True:
                print('\n')
                for num,option in enumerate(user_menu,start = 1):
                    move_cursor(6,'r')
                    valid_choices.append(num)
                    print(f'[{num}]: {option}')

                choice = int(input('\n\nPlease select an option: '))

                if choice not in valid_choices:
                    clear()
                    move_cursor(6,'r')

                    print('That was not a valid choice. Please try again.\n\n\n\n')

                elif choice == 1:

                    clear()
                    move_cursor(6,'r')
                    print(f':Change your password:\n\n')

                    move_cursor(6,'r')
                    new_pw = pwinput.pwinput(prompt="Please insert your new desired password (or leave blank to cancel): ", mask ='*')

                    if not new_pw: 
                        print('Cancelling. ')
                        continue

                    User.chpw(logged_user, new_pw)

                    move_cursor(6,'r')                
                    input("\n\nLogging your out for security purposes. Please log in again with your new password. Press Enter to continue.")
                    return None

                elif choice == 2:
                    clear()
                    print(f':View your Competency Progress:')
                    Results.view_user_competency(logged_user)
                    continue

                elif choice == 3:
                    clear()
                    print(f'Logging you out. Goodbye {user_name}')
                    return None

# active_user = User.select('john.i@infoxen.com')
# main_menu(active_user)

login()