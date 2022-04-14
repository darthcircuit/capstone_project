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