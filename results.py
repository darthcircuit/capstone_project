from database import *
def import_results():
    with open('results.csv') as csv_import:
        read_file = csv_import.readlines()


        # query = "INSERT INTO Assessment_Results (result_id, assess_id, user_id, assess_date, manager_id, score) VALUES (?,?,?,?,?,?)"

        header = read_file.pop(0)
        for row in read_file:
            row = row.split(',')
            print (row)
            db_cur.execute(query, row)
            db_con.commit()

import_results()