from random import choices
from database import db_con, db_cur
from date_lib import dt
from ansi_lib import *

class Assess:

    assess_list = ['Manager Evaluation', 'Peer Evaluation', 'Practical Skills', 'Self Evaluation']
    attr_fields = ['comp_id','name','date_created']

    def __init__(self, comp_id,name,date_created):

        self.comp_id = comp_id
        self.name = name
        self.date_created = date_created

    def create(competency):
  
        #Create Competency.create() will automatically run this code to create new assessments as comps are built.

        counter = 1

        while counter <= 4:
            assess_id = f'{competency.comp_id}.{counter}'
            assess_name = f'{competency.name} - {Assess.assess_list[counter-1]}'

            assess_db = [assess_id,competency.comp_id,assess_name,counter]
            query = "INSERT INTO Assessments (assess_id, comp_id, name, assess_type) VALUES (?,?,?,?)"
            db_cur.execute(query,assess_db)

            counter += 1
    
        db_con.commit()

    def view(select=False):

        clear()
        query = ("SELECT assess_id, name, assess_type FROM Assessments")

        comps = db_cur.execute(query).fetchall()
        choices_list = []
        bit_flip = 1

        set_font(text.bold, text.underline)
        print(f" {'ID':<10}| {'Assessment Name and Type':<75}")
        reset()
        for comp in comps:
            comp = [str(x) for x in comp]
            
            if bit_flip == 0:
                color = set_font(bg.magenta)
                bit_flip = 1
            else:
                color = set_font(bg.green)
                bit_flip = 0
            choices_list.append(comp[0])
            color
            print(f' {comp[0]:10}| {comp[1]:<75}', end="")
            reset()
            print()
        
        if select:
            return choices_list

    def edit(competency):

        counter = 1

        while counter <= 4:

            assess_name = f'{competency.name} - {Assess.assess_list[counter-1]}'
            assess_id = f'{competency.comp_id}.{counter}'

            assess_db = [assess_name,assess_id]
            query = "Update Assessments SET name = ? WHERE assess_id = ?"
            db_cur.execute(query,assess_db)
            db_con.commit()
            counter += 1
    
        