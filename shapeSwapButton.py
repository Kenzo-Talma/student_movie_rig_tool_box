import maya.cmds as cmds

def shapeSwap_func ():
    obList = cmds.ls(sl=True)

    ind = 0

    childrens = cmds.listRelatives(obList[0], children=True, s=True)
    color = cmds.getAttr(childrens[0] + '.overrideColor')
    shapeSize = cmds.getAttr(childrens[0] + '.lineWidth')

    for ob in obList:
        if ind == 0:
            childrens = cmds.listRelatives(ob, children=True, s=True)
            cmds.delete(childrens)

        else:
            obSh = cmds.listRelatives(ob, children=True, s=True)
            if len(obSh) > 1:
                for shape in obSh:
                    cmds.setAttr(ob + '|' + shape + '.overrideEnabled', 1)
                    cmds.setAttr(ob + '|' + shape + '.overrideColor', float(color))
                    cmds.setAttr(ob + '|' + shape + '.lineWidth', float(shapeSize))
                    cmds.parent(ob + '|' + shape, obList[0], s=True, r=True)
            else:
                for shape in obSh:
                    cmds.setAttr(shape + '.overrideEnabled', 1)
                    cmds.setAttr(shape + '.overrideColor', float(color))
                    cmds.setAttr(shape + '.lineWidth', float(shapeSize))
                    cmds.parent(obSh, obList[0], s=True, r=True)
            cmds.delete(ob)
        ind += 1
    cmds.select(obList[0])
    print("Shape swap done")

#shapeSwap_func()
