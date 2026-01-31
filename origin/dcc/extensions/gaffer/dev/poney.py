import Gaffer
import GafferUI
import GafferScene

def __iWantAPony( menu ) :

    scriptWindow = menu.ancestor( GafferUI.ScriptWindow )
    script = scriptWindow.scriptNode()

    with Gaffer.UndoContext( script ) :

        read = GafferScene.SceneReader( "Cow" )
        read["fileName"].setValue( "X:/projects/The_Rock/assets/chr/hulk/modeling/publishes/data/geometry__hulk__hulk_main/chr__hulk__hulk_main__v0010/alembic/chr__hulk__hulk_main__v0010.abc" )
        script.addChild( read )

        duplicate = GafferScene.Duplicate( "Herd" )
        duplicate["target"].setValue( "/geo" )
        duplicate["copies"].setValue( 7 )
        duplicate["transform"]["translate"]["x"].setValue( 16 )
        duplicate["transform"]["rotate"]["y"].setValue( 45 )
        duplicate["in"].setInput( read["out"] )
        script.addChild( duplicate )

    script.selection().clear()
    script.selection().add( duplicate )

GafferUI.ScriptWindow.menuDefinition(application).append( "/Help/I Want A Pony", { "command" : __iWantAPony } )