from dataclasses import field
from libs import *
import csv

def view_user_competency(to_csv = False):
    user = User.select()
    user = user.user_id
    query = '''
        SELECT DISTINCT (u.last_name ||', '|| u.first_name) as name, u.email as email, c.name as comp_name, c.comp_id as comp_id, a.assess_id as assess_id, AVG(r.score) as average_score
        FROM Users u
        JOIN Assessment_Results r
        ON u.user_id = r.user_id
        JOIN Assessments a
        ON r.assess_id = a.assess_id
        JOIN Competencies c
        ON a.comp_id = c.comp_id
        WHERE
        u.user_id = ?
        GROUP BY c.comp_id
        ORDER BY r.assess_id

    '''
    result = db_cur.execute(query, (user,))
    header = [name[0] for name in result.description]


    if to_csv:
        with open(f'./reports/User Competency Report - {user} {dt.today}.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            writer.writerows(result.fetchall())

view_user_competency(True)