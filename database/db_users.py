from common_utils.date_time import DateTime
from database import db_connection as mdbconn

class DbUsers:
    '''this class is used to create users in the database'''

    def __init__(self, first_name, last_name, personal_email, job_title, access_level):
        '''initialize the DbUsers class'''
        self.db = mdbconn.server.xchange
        self.main_domain = "origin.com"

        self.first_name = first_name
        self.last_name = last_name
        self.personal_email = personal_email
        self.job_title = job_title
        self.access_level = access_level


    def create_user(self):
        '''create a user in the database'''

        self.db.users.insert_one(
            {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "active": True,
                "access_type":self.access_level,
                "personal_email": self.personal_email,
                "job_title": self.job_title(),
                "user_name": self.user_internal(),
                "internal_email": self.user_company_email(),
                "date": DateTime().curr_date,
                "time": DateTime().curr_time
            }
        )
        print(" user for {} created!".format(self.first_name + " " + self.last_name))
        pass

    def user_company_email(self):
        '''create a user company email'''
        pass

    def user_internal(self):
        '''create a user internal name'''
        pass
