import maya.cmds as cmds


def makeSkinJointButton_func():
    jntList = cmds.ls(sl=True, type='joint')

    # cmds.group(n='SKIN_grp', em=True)
    parentJoint = 'face_M'

    if cmds.objExists(parentJoint):
        parentJoint = 'face_M'

    else:
        if cmds.objExists('Head_M'):
            cmds.select('Head_M')
            cmds.joint(n=parentJoint)
        else:
            parentJoint = 'deformation_grp'

    if len(jntList):

        if cmds.objExists('extraFace_M'):
            cmds.select(clear=True)

        else:
            cmds.select(parentJoint)
            cmds.joint(n='extraFace_M')

        # determine joint tags

        if 'lips' in jntList[0]:

            cmds.select(parentJoint)
            cmds.joint(n='lips_M')
            cmds.setAttr('lips_M.drawStyle', 2)
            # cmds.parent('lips_M', parentJoint)

            folderJoint = 'lips_M'

        elif 'smileLine_M' in jntList[0]:

            cmds.select(parentJoint)
            cmds.joint(n='smileLine_M')
            cmds.setAttr('smileLine_M.drawStyle', 2)
            # cmds.parent('lips_M', parentJoint)

            folderJoint = 'smileLine_M'

        elif 'cheek' in jntList[0]:

            cmds.select(parentJoint)
            cmds.joint(n='cheek_M')
            cmds.setAttr('cheek_M.drawStyle', 2)
            # cmds.parent('lips_M', parentJoint)

            folderJoint = 'cheek_M'

        elif 'smileLine' in jntList[0]:

            cmds.select(parentJoint)
            cmds.joint(n='eyeBrows_M')
            cmds.setAttr('eyeBrows_M.drawStyle', 2)
            # cmds.parent('lips_M', parentJoint)

            folderJoint = 'eyeBrows_M'

        elif 'nose' in jntList[0]:

            cmds.select(parentJoint)
            cmds.joint(n='nose_M')
            cmds.setAttr('nose_M.drawStyle', 2)
            # cmds.parent('lips_M', parentJoint)

            folderJoint = 'nose_M'

        elif 'eyeBrowsRibbon' in jntList[0]:

            cmds.select(parentJoint)
            cmds.joint(n='eyeBrowsRibbon_M')
            cmds.setAttr('eyeBrowsRibbon_M.drawStyle', 2)
            # cmds.parent('lips_M', parentJoint)

            folderJoint = 'eyeBrowsRibbon_M'

        elif 'tongue' in jntList[0]:

            cmds.select(parentJoint)
            cmds.joint(n='tongue_M')
            cmds.setAttr('tongue_M.drawStyle', 2)
            # cmds.parent('lips_M', parentJoint)

            folderJoint = 'tongue_M'

        else:
            folderJoint = 'extraFace_M'

        # parent skin joint

        for jnt in jntList:
            cmds.rename(jnt, 'SKIN_' + jnt)
            cmds.duplicate('SKIN_' + jnt, n=jnt)
            cmds.parent('SKIN_' + jnt, folderJoint)
            cmds.xform('SKIN_' + jnt, t=(0, 0, 0))
            cmds.xform('SKIN_' + jnt, ro=(0, 0, 0))
            cmds.setAttr('SKIN_' + jnt + '.inheritsTransform', 0)
            cmds.connectAttr(jnt + '.worldMatrix', 'SKIN_' + jnt + '.offsetParentMatrix')

            cmds.setAttr('SKIN_' + jnt + '.jointOrientX', 0)
            cmds.setAttr('SKIN_' + jnt + '.jointOrientY', 0)
            cmds.setAttr('SKIN_' + jnt + '.jointOrientZ', 0)

            cmds.setAttr(jnt + '.visibility', 0)