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
        comp_list = comp.split(',')
        query = ('INSERT INTO Competencies (name, date_created) VALUES (?,?)')
        db_cur.execute(query, comp_list)
        
    db_con.commit()

add_comps()

def add_users():
    with open('./schema/schema_users.csv') as users:
        read_users = users.readlines()
        
        #remove header row:
        read_users.pop(0)

    salt = bcrypt.gensalt()
    
    for user in read_users:
        user_list = (user.strip()).split(',')
        
        #convert plaintext password to hash
        hashed = bcrypt.hashpw(user_list[3].encode('utf'), salt)
        user_list[3] = hashed.decode()
        
        query = ("INSERT INTO Users (first_name,last_name,email,password,last_login,failed_logins,date_created,date_hired,passed_comps,user_type,status) VALUES (?,?,?,?,?,?,?,?,?,?,?)")   
        db_cur.execute(query, user_list)
    
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
