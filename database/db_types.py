class BranchTypes(object):
    @classmethod
    def build(cls):
        """return the correct string for the branch type"""
        return "build"

    @classmethod
    def sequences(cls):
        """return the correct string for the branch type"""
        return "shots"

    @classmethod
    def library(cls):
        '''return the correct string for the branch type'''
        return 'lib_asset'

    @classmethod
    def reference(cls):
        '''return the correct string for the branch type'''
        return 'ref_asset'


class CategoryTypes(object):
    @classmethod
    def characters(cls):
        """return the correct string for the category type"""
        return "characters"

    @classmethod
    def props(cls):
        '''return the correct string for the category type'''
        return "props"

    @classmethod
    def environments(cls):
        '''return the correct string for the category type'''
        return 'environments'


class EntityTypes(object):

    @classmethod
    def build(cls):
        '''return the correct string for the entity type'''
        return "build"

    @classmethod
    def shot(cls):
        '''return the correct string for the entity type'''
        return "shots"


class TaskTypes(object):

    @classmethod
    def characters(cls):
        '''return the correct string for the task type'''
        return "character"

    @classmethod
    def props(cls):
        '''return the correct string for the task type'''
        return 'prop'

    @classmethod
    def environments(cls):
        '''return the correct string for the task type'''
        return 'environment'

    @classmethod
    def shots(cls):
        '''return the correct string for the task type'''
        return 'shot'



if __name__ == "__main__":
    '''test the module '''
    x = BranchTypes.sequences()
    print (x)