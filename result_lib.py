from user_lib import User
from assess_lib import Assess
class Results:

    result_attr = ['result_id','assess_id','user_id','assess_date','manager_id','score']

    def __init__(self,attr_dict):

        for attr in Results.result_attr:
            setattr(self,attr,attr_dict[attr])

        self.attr = [self.result_id, self.assess_id, self.user_id, self.assess_date, self.manager_id, self.score]

    def add_result():
        result_dict = {}
        user = User.select()
        assess = Assess.view(True)
        manager = User.view('manager','select')

        #as a reminder, assess_id is created based on comp_id and assess_type.
        #result_id is determined based off of assess_id, user_id, and attempt number
        #for a second attempt for assessment 14.2 for user 12, the result_d == 14.2.12.2
        result_dict['result_id'] = f'{assess.assess_id}.{user.user_id}.{"Insert attempt # here"}'




