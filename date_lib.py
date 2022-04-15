from datetime import date, timedelta
import re

today = date.today()

class date_time:
    
    def get_date():
            while True:

                date_input = input('Type in the date (or leave blank if unknown) using this format: YYYY-MM-DD\n')
                    
                if re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', date_input):
                    return date_input
                
                elif not date_input:
                    return None
                else:
                    print('That format was incorrect. Please Try again.')
    