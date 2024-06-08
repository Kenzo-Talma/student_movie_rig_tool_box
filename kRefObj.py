import maya.cmds as cmds

def kRefObj_func():

    objList = cmds.ls(sl=True, type="transform")

    for obj in objList:
        overrideAttr = cmds.getAttr(obj + ".overrideEnabled")
        overrideTypeAttr = cmds.getAttr(obj + ".overrideDisplayType")

        if overrideAttr == 0:
            cmds.setAttr(obj + ".overrideEnabled", 1)

        if overrideTypeAttr == 2:
            cmds.setAttr(obj + ".overrideDisplayType", 0)
        else:
            cmds.setAttr(obj + ".overrideDisplayType", 2)
