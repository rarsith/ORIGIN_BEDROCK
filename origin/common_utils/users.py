import getpass

class Users(object):

    @staticmethod
    def curr_user():
        username = getpass.getuser()
        return username