import maya.cmds as cmds

def poseInterpollatorConnect():
    jnt = cmds.ls(sl=True, type='joint')[0]
    poseInt = cmds.ls(sl=True, type = 'poseInterpolator')[0]

    cmds.createNode('decomposeMatrix', n=jnt + '_decomposeMatrix')
    cmds.createNode('clamp', n=jnt + '_clamp')
    cmds.createNode('composeMatrix', n=jnt + '_composeMatrix')

    cmds.connectAttr(jnt + '.matrix', jnt + '_decomposeMatrix.inputMatrix', f=True)

    cmds.connectAttr(jnt + '_decomposeMatrix.outputTranslate', jnt + '_composeMatrix.inputTranslate', f=True)
    cmds.connectAttr(jnt + '_decomposeMatrix.outputQuat', jnt + '_composeMatrix.inputQuat', f=True)
    cmds.connectAttr(jnt + '_decomposeMatrix.outputShear', jnt + '_composeMatrix.inputShear', f=True)
    cmds.connectAttr(jnt + '_decomposeMatrix.outputScale', jnt + '_composeMatrix.inputScale', f=True)

    cmds.connectAttr(jnt + '_decomposeMatrix.outputRotate', jnt + '_clamp.input', f=True)

    cmds.connectAttr(jnt + '_clamp.output', jnt + '_composeMatrix.inputRotate', f=True)

    cmds.connectAttr(jnt + '_composeMatrix.outputMatrix', poseInt + '.driver[0].driverMatrix', f=True)