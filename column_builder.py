from ansi_lib import *

    
test_dict = [
    {
        'first_name': 'Joe',
        'last_name': 'Ipson',
        'email': 'joe.i@infoxen.com',
        'password': '$2b$12$soup.',
        'date_created': '2022-04-20',
        'date_hired': '2022-04-04',
        'user_type': 1
        },

    {
        'first_name': 'John',
        'last_name': 'Ipson',
        'email': 'john.i@infoxen.com',
        'password': '$2b$12$wow.',
        'date_created': '2022-04-20',
        'date_hired': '2022-04-04',
        'user_type': 0
        },

    {
        'first_name': 'Rebecca',
        'last_name': 'Ipson',
        'email': 'rebecca.i@infoxen.com',
        'password': '$2b$12$flowers.',
        'date_created': '2022-04-20',
        'date_hired': '2022-04-04',
        'user_type': 0
        },
            {
        'first_name': 'Joe',
        'last_name': 'Ipson',
        'email': 'joe.i@infoxen.com',
        'password': '$2b$12$soup.',
        'date_created': '2022-04-20',
        'date_hired': '2022-04-04',
        'user_type': 1
        },

    {
        'first_name': 'John',
        'last_name': 'Ipson',
        'email': 'john.i@infoxen.com',
        'password': '$2b$12$wow.',
        'date_created': '2022-04-20',
        'date_hired': '2022-04-04',
        'user_type': 0
        },

    {
        'first_name': 'Rebecca',
        'last_name': 'Ipson',
        'email': 'rebecca.i@infoxen.com',
        'password': '$2b$12$flowers.',
        'date_created': '2022-04-20',
        'date_hired': '2022-04-04',
        'user_type': 0
        },
            {
        'first_name': 'Joe',
        'last_name': 'Ipson',
        'email': 'joe.i@infoxen.com',
        'password': '$2b$12$soup.',
        'date_created': '2022-04-20',
        'date_hired': '2022-04-04',
        'user_type': 1
        },

    {
        'first_name': 'John',
        'last_name': 'Ipson',
        'email': 'john.i@infoxen.com',
        'password': '$2b$12$wow.',
        'date_created': '2022-04-20',
        'date_hired': '2022-04-04',
        'user_type': 0
        },

    {
        'first_name': 'Rebecca',
        'last_name': 'Ipson',
        'email': 'rebecca.i@infoxen.com',
        'password': '$2b$12$flowers.',
        'date_created': '2022-04-20',
        'date_hired': '2022-04-04',
        'user_type': 0
        }
    ]

def is_even(number):
    if number % 2 == 0: return True
    elif number == 0: return True
    return False

def build_column(dataset_list):

    col_width_dict = {}

    col_name_choices = {
        #Users
        'user_id':"User ID",
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'email': 'Email Address',
        'password': 'Password',
        'last_login': 'Last Login',
        'failed_logins': 'Failed Logins',
        'date_hired': 'Date Hired',
        'passed_comps': 'Passed Competencies',
        'user_type': 'User Type',
        'status': 'Status',

        #Competencies
        'comp_id':'Competency ID',

        #Assessments
        'assess_id':'Assessment ID',
        
        #Shared
        'date_created': 'Date Created',
        'name': 'Name',

        #Results
        'result_id':'Result ID',
        'assess_date':'Assessment Date',
        'manager_id':'Manager ID',
        'score':'Score'
        
    }

    rows = []
    #import a list of dictionaries and unpack
    for data_dict in dataset_list:

        #find column width
        header = list(data_dict.keys())
        row = []
        for col,val in data_dict.items():
        
            try:
                col_width_dict[col] = max(len(col), len(str(val)), col_width_dict[col])

            except:
                col_width_dict[col] = max(len(col), len(str(val)))

            row.append(val)


        #prepare data for print
        rows.append(row)



    #trial column printer:
    #print one column at a time until all data is done
    #print header first
    num_rows = len(rows)
    print('\n' * (num_rows))
    move_cursor(num_rows,'u')    


    for col_num, col_name in enumerate(header):
        row_num = 0

        #set column width:
        width = col_width_dict[col_name]+2
        
        #header
        set_font(text.bold, text.underline, bg.black)
        print(f'{col_name:<{width}} |', end = '')
        reset()

        while row_num < num_rows:
            row = rows[row_num]
            if is_even(row_num):
                color = set_font(bg.blue)
            else:
                color = set_font(bg.cyan)
            row_num += 1
            
            
            move_cursor(1,'d')
            move_cursor(width+2,'l')
            
            color
            print(f'{row[col_num]:<{width}} |', end = '')
            reset()

        move_cursor(row_num, 'u')

    if col_num == len(header)-1:
        print('\n' * (num_rows))


build_column(test_dict)

