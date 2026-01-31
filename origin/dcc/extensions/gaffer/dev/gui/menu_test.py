# import LDTGafferUtils

import functools

import GafferUI

print ("LDTGAFFER:startup:gui:menu")

GafferUI.ScriptWindow.menuDefinition(application).append(
	"/LDT/tools/" + "Export extension",
	{
		"command" : "", #stream data during loop
		"label" : "Export Extension"
	}
)

GafferUI.ScriptWindow.menuDefinition(application).append(
	"/LDT/tools/" + "registerAnnotation",
	{
		"command" : "", #stream data during loop
		"label" : "registerAnnotation"
	}
)

GafferUI.ScriptWindow.menuDefinition(application).append(
	"/LDT/tools/" + "registerEditScopeIncludeInNavigationMenu",
	{
		"command" : "", #stream data during loop
		"label" : "registerEditScopeIncludeInNavigationMenu"
	}
)