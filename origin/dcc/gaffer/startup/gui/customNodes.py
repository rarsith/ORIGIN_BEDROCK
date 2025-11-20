import Gaffer
import GafferUI
import os

def __macbethTexture() :

    return Gaffer.Reference( "MacbethTexture" )

def __macbethTexturePostCreator( node, menu ) :

    node.load(
            os.path.expandvars( "$GAFFER_ROOT/resources/examples/references/macbethTexture.grf" )
    )

nodeMenu = GafferUI.NodeMenu.acquire( application )
nodeMenu.append(
    path = "/Custom/MacbethTextureXX",
    nodeCreator = __macbethTexture,
    postCreator = __macbethTexturePostCreator,
    searchText = "MacbethTexture"
)