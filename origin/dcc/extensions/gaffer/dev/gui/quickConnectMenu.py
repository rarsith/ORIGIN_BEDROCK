import imath
import IECore
import Gaffer
import GafferUI

__quickConnectPlugPath = None

def __quickConnectPlugContextMenu(nodeGraph, plug, menuDefinition):
    if plug.direction() != Gaffer.Plug.Direction.In:
        return

    def __isQuickConnectPlug(plug):
        global __quickConnectPlugPath

        if __quickConnectPlugPath is None:
            return False
        return plug.isSame(plug.node().scriptNode().descendant(__quickConnectPlugPath))

    def __updateQuickConnectPlug(plug, enable):
        global __quickConnectPlugPath

        if __quickConnectPlugPath is not None:
            oldPlug = plug.node().scriptNode().descendant(__quickConnectPlugPath)
            if oldPlug:
                Gaffer.Metadata.registerValue(oldPlug, "nodule:color", None)

            if not enable:
                __quickConnectPlugPath = None
                return
        Gaffer.Metadata.registerValue(plug, "nodule:color", imath.Color3f(0,1,0))
        __quickConnectPlugPath = plug.relativeName(plug.node().scriptNode())

    menuDefinition.prepend(
        "Target for Quick COnnect", {
            "command": IECore.curry(__updateQuickConnectPlug, plug),
            "checkBox": IECore.curry(__isQuickConnectPlug, plug)
        }
    )

GafferUI.NodeGraph.plugContextMenuSignal().connect(__quickConnectPlugContextMenu, scoped = False)

def __quickConnectPlugs(scriptWindow):
    global __quickConnectPlugPath
    if __quickConnectPlugPath is None:
        return None

    if scriptWindow.scriptNode().selection().size() != 1:
        return None

    quickConnectPlug = scriptWindow.scriptNode().descendant(__quickConnectPlugPath)
    if quickConnectPlug is None:
        return None

    #check for the "out" plug first
    node = scriptWindow.scriptNode().selection()[0]
    out = node.getChild("out")
    if out is not None and out.direction() != Gaffer.Plug.Direction.Out:
        if quickConnectPlug.acceptsInput(out):
            return (quickConnectPlug, out)

    #check the remaining out plugs
    outPlugs = [x for x in node.children(Gaffer.Plug) if x.direction() == Gaffer.Plug.Direction.Out]
    for out in outPlugs:
        if quickConnectPlug.acceptsInput(out):
            return (quickConnectPlug, out)

    #Check for children of the out plug
    #This was required for OSL nodes to quick connect correctly
    for child in out.children():
        if quickConnectPlug.acceptsInput(child):
            return (quickConnectPlug, child)

    return None

def __quickCOnnect(menu):
    scriptWindow = menu.ancestor(GafferUI.ScriptWindow)
    (quickConnectPlug, out) = __quickConnectPlugs(scriptWindow)

    with Gaffer.UndoScope(scriptWindow.scriptNode()):
        quickConnectPlug.setInput(out)

def __canQuickConnect(menu):
    return True if __quickConnectPlugs(menu.ancestor(GafferUI.ScriptWindow)) else False

GafferUI.ScriptWindow.menuDefinition(application).append("/Tools/Quick Connect", {"command": __quickCOnnect,  "shortCut": "P", "active": __canQuickConnect})