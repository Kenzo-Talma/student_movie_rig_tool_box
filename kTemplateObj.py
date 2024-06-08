import maya.cmds as cmds

def kTemplateObj_func():

    lst = cmds.ls(sl=True, type="transform")

    for obj in lst:
        attribute = cmds.getAttr(obj + ".template")

        if attribute == 0:
            cmds.setAttr(obj + ".template", 1)
        else:
            cmds.setAttr(obj + ".template", 0)
