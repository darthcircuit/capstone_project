def create_mock_courses():
    with open('mock_courses.csv', 'r') as mock_course_data:
        records = mock_course_data.readlines()
        connection = sqlite3.connect('my_customers.db')
        cursor = connection.cursor()

        for record in records:
            record = record.strip()
            record_list = record.split(',')
            cursor.execute('INSERT INTO Courses (name, description) VALUES (?,?)',(record_list))
        
        connection.commit()

def create_mock_users():
    with open('mock_users.csv', 'r') as mock_user_data:
        records = mock_user_data.readlines()
        connection = sqlite3.connect('my_customers.db')
        cursor = connection.cursor()

        for record in records:
            record = record.strip()
            record_list = record.split(',')
            cursor.execute('INSERT INTO People (first_name, last_name, email, phone, password, address, city, state, postal_code,active) VALUES (?,?,?,?,?,?,?,?,?,?)',(record_list))
        
        connection.commit()




class User:
    desired_info = ['user_id','first_n','last_n','city','state','email','password','date_created','birthday','age','admin']
    connection = sqlite3.connect('class_users.db')
    db_cursor = connection.cursor()
    active_user = ''
    selected_user = ''

    def __init__(self,user_info_dict,info = desired_info):

        for attr in info:
            setattr(self, attr, user_info_dict[attr])

        self.attributes = [self.user_id,self.first_n,self.last_n,self.city,self.state,self.email,self.password,self.date_created,self.birthday,self.age,self.admin]



    def create_user():

            info_dict = {}
            for info in User.desired_info:
                        
                if info == 'birthday':
                    print(f'{info}: ', end='')
                    info_dict[info] = User.get_date()

                elif info == 'age':
                    info_dict[info]= User.age_calc(info_dict['birthday'])

                elif info == 'password':
                    #this will generate a random secure password and then encrypt it.
                    salt = bcrypt.gensalt()
                    passwd = secrets.token_urlsafe(10).encode("utf-8")
                    hashed = bcrypt.hashpw(passwd, salt)
                    info_dict[info] = hashed.decode('utf-8')

                    print(f'Password has been set to {passwd.decode()} \nShare this with the user. They can change it later.')

                elif info == 'admin':
                    admin = input('If this user is going to be an administrator, enter 1. Otherwise press enter. ')
                    if admin == '1':
                        info_dict[info] = 1
                    else:
                        info_dict[info] = 0

                elif info == 'date_created':
                    info_dict[info] = User.get_date(True)

                elif info == 'user_id':
                    while True:
                        info_dict[info] = random.randint(10000,99999)
                        unique_id = User.get_unique(info_dict['user_id'])
                        
                        #reroll user_id if not unique
                        if not unique_id:
                            continue
                        else:
                            break

                elif info == 'email':
                    while True:
                        info_dict['email'] = input(f'{info}: ')
                    
                        #if non-unique email entered, close
                        unique_email = User.get_unique(info_dict['email'])
                        if not unique_email:
                            print(f'User with email{info_dict["email"]} already exists in database.  Please insert a different one.')
                        else:
                            break

                else:    
                    info_dict[info] = input(f'{info}: ')

            return User(info_dict)
            