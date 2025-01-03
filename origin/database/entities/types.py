class EntityTypes:

    @classmethod
    def asset(cls):
        '''return the correct string for the entity type'''
        return "asset"

    @classmethod
    def group(cls):
        '''return the correct string for the entity type'''
        return "group"

    @classmethod
    def publish(cls):
        '''return the correct string for the entity type'''
        return "publish"

    @classmethod
    def work_file(cls):
        '''return the correct string for the entity type'''
        return "work_file"

    @classmethod
    def stream(cls):
        return "stream"

    @classmethod
    def stack(cls):
        return "stack"

    @classmethod
    def reference(cls):
        '''return the correct string for the entity type'''
        return "reference"

    @classmethod
    def lib_asset(cls):
        '''return the correct string for the entity type'''
        return "lib_asset"

    @classmethod
    def package(cls):
        '''return the correct string for the entity type'''
        return "package"

    @classmethod
    def template(cls):
        '''return the correct string for the entity type'''
        return "template"


class TaskTypes:

    @classmethod
    def concept(cls):
        '''return the correct string for the entity type'''
        return "concept"

    @classmethod
    def fx(cls):
        '''return the correct string for the entity type'''
        return "fx"

    @classmethod
    def character_fx(cls):
        '''return the correct string for the entity type'''
        return "character_fx"

    @classmethod
    def groom(cls):
        '''return the correct string for the entity type'''
        return "groom"

    @classmethod
    def modeling(cls):
        '''return the correct string for the entity type'''
        return "modeling"

    @classmethod
    def rigging(cls):
        '''return the correct string for the entity type'''
        return "rigging"

    @classmethod
    def shading(cls):
        '''return the correct string for the entity type'''
        return "shading"

    @classmethod
    def texturing(cls):
        '''return the correct string for the entity type'''
        return "texturing"

    @classmethod
    def tracking(cls):
        '''return the correct string for the entity type'''
        return "tracking"

    @classmethod
    def layout(cls):
        '''return the correct string for the entity type'''
        return "layout"

    @classmethod
    def rotomation(cls):
        '''return the correct string for the entity type'''
        return "rotomation"

    @classmethod
    def animation(cls):
        '''return the correct string for the entity type'''
        return "animation"

    @classmethod
    def shot_sculpt(cls):
        '''return the correct string for the entity type'''
        return "shot_sculpt"

    @classmethod
    def lighting(cls):
        '''return the correct string for the entity type'''
        return "lighting"

    @classmethod
    def rendering(cls):
        '''return the correct string for the entity type'''
        return "rendering"

    @classmethod
    def compositing(cls):
        '''return the correct string for the entity type'''
        return "compositing"

    @classmethod
    def template(cls):
        '''return the correct string for the entity type'''
        return "template"

    def all_types(self):
        return [self.concept(),
                self.modeling(),
                self.texturing(),
                self.rigging(),
                self.groom(),
                self.shading(),
                self.character_fx(),
                self.fx(),
                self.tracking(),
                self.layout(),
                self.rotomation(),
                self.animation(),
                self.character_fx(),
                self.shot_sculpt(),
                self.lighting(),
                self.rendering(),
                self.compositing(),
                self.template()]

    def all_build_types(self):
        return [
            self.concept(),
            self.modeling(),
            self.texturing(),
            self.rigging(),
            self.groom(),
            self.shading(),
            self.character_fx(),
            self.fx()
        ]

    def all_shot_types(self):
        return [
            self.tracking(),
            self.layout(),
            self.rotomation(),
            self.animation(),
            self.character_fx(),
            self.shot_sculpt(),
            self.lighting(),
            self.rendering(),
            self.compositing()
        ]



if __name__ == "__main__":
    '''test the module '''
    x = EntityTypes.asset()
    print(x)
