from database import db_con, cursor
import date_lib

print(date_lib.today())

cursor.execute('SELECT * FROM USERS').fetchall()

