import maya.cmds as cmds

def shapeSize_func():
    shapeSize = input('shape size ?')
    obList = cmds.ls(sl=True, type='transform')

    for ob in obList:
        shapeList = []
        shapes = cmds.listRelatives(ob, c=True, ad=False, s=True)

        for shape in shapes:
            shapeList.append(shape)

        if len(shapeList)>1:
            for shape in shapeList:
                cmds.setAttr(ob + '|' + shape + '.lineWidth', float(shapeSize))
        else:
            for shape in shapeList:
                cmds.setAttr(shape + '.lineWidth', float(shapeSize))