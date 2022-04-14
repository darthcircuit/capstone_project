import pwinput
import secrets
import random
import bcrypt
import date_lib
import sql_db as db


class User:
    user_attr = ['user_id','first_name','last_name','email','password','last_login','failed_logins','date_created','date_hired','passed_comps','user_type','status']

    active_user = ''
    selected_user = ''
    
        