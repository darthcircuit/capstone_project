from datetime import date, timedelta
import re


class dt:
    
    today = date.today()
    
    def get_date():
            while True:

                date_input = input('Type in the date (or leave blank if unknown) using this format: YYYY-MM-DD\n')
                    
                if re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', date_input):
                    print()
                    return date_input
                
                elif not date_input:
                    return None
                else:
                    print('That format was incorrect. Please Try again.')
    