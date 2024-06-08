import maya.cmds as cmds

def ShapeColor_func(color):
    obList = cmds.ls(sl=True, type='transform')


    for ob in obList:
        shapeList = []
        shapes = cmds.listRelatives(ob, c=True, ad=False, s=True)

        for shape in shapes:
            shapeList.append(shape)

        if len(shapeList) > 1:
            for shape in shapeList:
                cmds.setAttr(ob + '|' + shape + '.overrideEnabled', 1)
                cmds.setAttr(ob + '|' + shape + '.overrideColor', float(color))
        else:
            for shape in shapeList:
                cmds.setAttr(shape + '.overrideEnabled', 1)
                cmds.setAttr(shape + '.overrideColor', float(color))
