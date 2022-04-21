from random import choices
from database import db_con, db_cur
from date_lib import dt
from ansi_lib import *
from assess_lib import Assess
class Competencies:

    attr_fields = ['comp_id','name','date_created']

    def __init__(self, comp_id,name,date_created):

        self.comp_id = comp_id
        self.name = name
        self.date_created = date_created

    def create():

        name = input('Please enter a name for this competency: ')
        date_created = f'{dt.today}'
        
        query = ("INSERT INTO Competencies (name,date_created) VALUES (?,?)")
        db_cur.execute(query, (name, date_created))

        db_con.commit()

        query = (f"SELECT comp_id FROM Competencies WHERE name ='{name}'")
        comp = db_cur.execute(query).fetchone()

        comp_id = comp[0] 

        new_comp = Competencies(comp_id, name, date_created)

        Assess.create(new_comp)

        return new_comp

    def view(select=False):

        query = ("SELECT comp_id, name, date_created FROM Competencies")

        comps = db_cur.execute(query).fetchall()
        choices_list = []
        bit_flip = 1

        set_font(text.bold, text.underline)
        print(f" {'ID':<5}| {'Name':<30}| {'Date Created':<14}")
        reset()
        for comp in comps:
            comp = [str(x) for x in comp]
            
            if bit_flip == 0:
                color = set_font(bg.magenta)
                bit_flip = 1
            else:
                color = set_font(bg.cyan)
                bit_flip = 0
            choices_list.append(comp[0])
            color
            print(f' {comp[0]:5}| {comp[1]:<30}| {comp [2]:<14}', end="")
            reset()
            print()
        
        if select:
            return choices_list
           
    def edit():

        choices_list = Competencies.view(True)


        while True:
            edit_sel = input('Enter the Competency ID that you would like to edit: ')
            if edit_sel in choices_list:
                break
            else:
                print('Not a valid selection. Please try select a different option.')

        col_name = input('What would you like to name this competency? ')
        
        print("When was this competency Created?\n")
        col_date = dt.get_date()

        query = (f"UPDATE Competencies SET name = '{col_name}', date_created = '{col_date}' WHERE comp_id = '{edit_sel}'")
        # params = (col_name,col_date,edit_sel)

        db_cur.execute(query)
        db_con.commit()

        comp_object = Competencies(edit_sel,col_name,col_date)

        Assess.edit(comp_object)