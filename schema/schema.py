from database import db_cur, db_con
import bcrypt



def create_schema():
    with open('./schema/schema_tables.txt', 'r') as schema:
        queries = schema.readlines()
    
    for query in queries:
        db_cur.execute(query)

    db_con.commit()

create_schema()

def add_comps():
    with open('./schema/schema_comp.csv') as comps:
        read_comps = comps.readlines()
        
    #remove header row:
    read_comps.pop(0)

    for comp in read_comps:
        comp_list = comp.strip().split(',')
        query = ('INSERT INTO Competencies (name, date_created) VALUES (?,?)')
        db_cur.execute(query, comp_list)
        
    db_con.commit()

add_comps()

def add_users():
    with open('./schema/schema_users.csv', encoding='utf-8-sig') as users:
        read_users = users.readlines()
        
        #remove header row:
        header = read_users.pop(0)
        header = header.strip().split(',')


    salt = bcrypt.gensalt()


    
    for row in read_users:
        row = row.strip().split(',')
        user_dict = dict(zip(header,row))

        new_header = []
        row_list = []
        var_list = []

        for key,value in user_dict.items():
            if value:
                if key == 'password':
                    #convert plaintext password to hash
                    hashed = bcrypt.hashpw(value.encode('utf'), salt)
                    value = hashed.decode()

                new_header.append(key)           
                row_list.append(value)
                var_list.append('?')

        new_header = f'({",".join(new_header)})'
        var_list =f'({",".join(var_list)})'

        query = (f"INSERT INTO Users {new_header} VALUES {var_list}")   
        db_cur.execute(query, row_list)
        db_con.commit()

add_users()

def add_assesments():
    with open('./schema/schema_comp.csv') as comps:
        read_comps = comps.readlines()

    #remove header row:
    read_comps.pop(0)
    

    assess_list = ['Manager Evaluation', 'Peer Evaluation', 'Practical Skills', 'Self Evaluation']
    assessments = {}

        
    for comp_id,comp in enumerate(read_comps, start=1):
        counter = 1
        comp_list = comp.strip().split(',')

        while counter <= 4:
            assess_id = f'{comp_id}.{counter}'
            assess_name = f'{comp_list[0]} - {assess_list[counter-1]}'
            
            #Creates a dictionary for all the generated assesment names and corresponding ID's    
            assessments[assess_id] = assess_name

            #parameters for inserting into db
            assess_db = [assess_id,comp_id,assess_name,counter]
            query = "INSERT INTO Assessments (assess_id, comp_id, name, assess_type) VALUES (?,?,?,?)"
            db_cur.execute(query,assess_db)

            counter += 1
    
    db_con.commit()
    # print(assessments)

    #Write dictionary to db as ID, name


add_assesments()
