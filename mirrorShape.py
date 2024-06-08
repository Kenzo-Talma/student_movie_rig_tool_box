import maya.cmds as cmds

def mirrorShape_func(origSide, endSide):
    #origSide = input('search for ?')
    #endSide = input('replace by ?')

    obList = cmds.ls(sl=True, type='transform')
    # shapeList = []

    for ob in obList:
        shapeList = cmds.listRelatives(ob, c=True, ad=False, s=True)

        n = 0
        obInv = ob.replace(origSide, endSide)

        for shape in shapeList:
            cvCount = cmds.getAttr(shape + '.spans')
            cvList = []
            shapeInv = shape.replace(origSide, endSide)

            for i in range(cvCount):
                cv = ob + '.cv[' + str(i) + ']'
                cvList.append(cv)

            cmds.duplicate(shape)

            # cmds.rename(shape.split('Shape') + '1', obInv)
            cmds.parent(ob + '1Shape', obInv, s=True, r=True)
            cmds.delete(shapeInv)

            cmds.rename(ob + '1Shape', shapeInv)
            cmds.delete(ob + '1')

            '''for cv in cvList:
                cvPos = cmds.xform(cv, q=True, t=True, ws=True, a=True)

                cvInv = cv.replace(origSide, endSide)

                cvInvPos = (-cvPos[0], cvPos[1], cvPos[2])

                cmds.xform(cvInv, t=cvInvPos, ws=True, a=True)'''

            colorIndex = cmds.getAttr(shape + '.overrideColor')
            shapeSize = cmds.getAttr(shape + '.lineWidth')

            cmds.setAttr(shapeInv + '.overrideEnabled', 1)
            cmds.setAttr(shapeInv + '.overrideColor', colorIndex)
            cmds.setAttr(shapeInv + '.lineWidth', shapeSize)


        """for shape in shapes:
            shapeList.append(shape)"""


    """for shape in shapeList:
        cvCount = cmds.getAttr(shape + '.spans')
        cvList = []

        for i in range (cvCount):
            cv = shape.split('Shape')[0] + 'cv.[' + str(i) + ']'
            cvList.append(cv)

        cmds.duplicate(shape)
        obInv = shape.split('Shape').replace(origSide, endSide)
        #cmds.rename(shape.split('Shape') + '1', obInv)

        cmds.parent(shape + '1', obInv, s=True, r=True)
        cmds.rename(shape + '1', obInv + 'Shape')

        for cv in cvList :
            cvPos = cmds.xform(cv, q=True, t=True, ws=True, a=True)

            cvInv = cv.replace(origSide, endSide)
            
            cmds.xform(cvInv, t=cvPos, ws=True, a=True)"""