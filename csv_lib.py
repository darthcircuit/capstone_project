def bulk_add_people():
    with open(f'People.csv', 'r') as user_data:
        records = user_data.readlines()
        connection = sqlite3.connect('my_students.db')
        cursor = connection.cursor()
        records.pop(0)

        for record in records:
            record = record.strip()
            record_list = record.split(',')
            if record[0].isalnum():
                cursor.execute('INSERT OR REPLACE INTO People (person_id, first_name, last_name, email, phone, password, address, city, state, postal_code,active) VALUES (?,?,?,?,?,?,?,?,?,?,?)',(record_list))
            else:
                cursor.execute('INSERT OR REPLACE INTO People (first_name, last_name, email, phone, password, address, city, state, postal_code,active) VALUES (?,?,?,?,?,?,?,?,?,?)',(record_list[1::]))
        
        connection.commit()



def bulk_export_all():
    
    todays_date = f'{pick_day(True,False)}'.split()[0]
    tables = ['People', 'Courses', 'Cohorts', 'Student_Cohort_Registrations']

    for tab in tables:
        data = exec_query(f'SELECT * FROM {tab}','','all')
        header = exec_query(f"SELECT group_concat(name, ', ') FROM pragma_table_info('{tab}')",'','one')
        data.insert(0, header) 

        with open(f'{todays_date}_{tab}.csv', 'w') as export:
            writer = csv.writer(export)
            writer.writerows(data)