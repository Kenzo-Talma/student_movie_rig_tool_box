import sys
import maya.cmds as cmds
import maya.OpenMayaUI as mui
from PySide2 import QtGui, QtCore, QtWidgets
import shiboken2
import math


def mayaMainWindow():
    mainWindowPtr = mui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return (shiboken2.wrapInstance(int(mainWindowPtr), QtWidgets.QWidget))
    else:
        return (shiboken2.wrapInstance(long(mainWindowPtr), QtWidgets.QWidget))


class wireBasedCurveRibbonMakerWin(QtWidgets.QDialog):

    def __init__(self, parent=mayaMainWindow()):
        super(wireBasedCurveRibbonMakerWin, self).__init__(parent)
        self.ribbonName = None
        self.edgeloop = None
        self.parentJoint = None
        self.setWindowTitle("Ribbon maker")
        self.setMinimumWidth(200)
        # self.setMinimumHeight(500)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.createWidget()
        self.createLayout()

    # functions

    def ribbonNameLineEdit_func(self):
        self.ribbonName = self.ribbonNameLineEdit.text()

    def edgeLoopCheckbox_func(self):
        self.edgeloop = cmds.ls(sl=True)
        #print(self.edgeloop)

    def parentJointCheckbox_func(self):
        self.parentJoint = cmds.ls(sl=True)[0]

    def buildButton_func(self):
        curveName = self.ribbonName + '_crv'
        jointNumber = 1
        parentLoc = self.ribbonName + '_loc'

        for edge in self.edgeloop:
            jointNumber += 1

        cmds.select(clear=True)
        cmds.select(self.edgeloop)
        cmds.polyToCurve(n=curveName, form=2, degree=3, conformToSmoothMeshPreview=1)
        cmds.DeleteHistory(curveName)

        cmds.spaceLocator(n=parentLoc)
        parentJointPos = cmds.xform(self.parentJoint, q=True, t=True, ws=True, a=True)
        cmds.xform(parentLoc, t=parentJointPos, ws=True, a=True)

        cmds.group(em=True, n=curveName + '_jnt_grp')

        for i in range(jointNumber):
            cmds.select(clear=True)
            jointName = self.ribbonName + '_' + str(i + 1) + '_jnt'
            cmds.joint(n=jointName)
            cmds.group(jointName, n=jointName + '_offset')
            cmds.group(jointName + '_offset', n=jointName + '_grp')

            cmds.connectAttr(curveName + 'Shape.editPoints[' + str(i) + ']', jointName + '_grp.translate', f=True)
            cmds.tangentConstraint(curveName, jointName + '_grp', aimVector=(1, 0, 0), upVector=(0, 0, 1),worldUpType='object', worldUpVector=(0, 1, 0), worldUpObject=parentLoc)

            cmds.setAttr(jointName + ".jointOrientX", 0)
            cmds.setAttr(jointName + ".jointOrientY", 0)
            cmds.setAttr(jointName + ".jointOrientZ", 0)

            cmds.parent(jointName + '_grp', curveName + '_jnt_grp')

    def controlGuidesButton_func(self):
        diamond = [(1, 0, 0),
                   (0, 1, 0),
                   (-1, 0, 0),
                   (0, -1, 0),
                   (1, 0, 0),
                   (0, 0, 1),
                   (-1, 0, 0),
                   (0, 0, -1),
                   (1, 0, 0),
                   (0, 0, 1),
                   (0, 1, 0),
                   (0, 0, -1),
                   (0, -1, 0),
                   (0, 0, 1)]

        buildCurve = self.ribbonName + '_build_crv'
        ctrlCurve = self.ribbonName + '_ctrl_crv'

        ctrlList = [self.ribbonName + 'InnerBack_ctrl',
                    self.ribbonName + 'Back_ctrl',
                    self.ribbonName + 'OuterBack_ctrl',
                    self.ribbonName + 'Outer_ctrl',
                    self.ribbonName + 'OuterFront_ctrl',
                    self.ribbonName + 'Front_ctrl',
                    self.ribbonName + 'InnerFront_ctrl',
                    self.ribbonName + 'Inner_ctrl']

        cmds.circle(n=buildCurve, nr=(0, 1, 0))
        cmds.circle(n=ctrlCurve)
        cmds.group(ctrlCurve, n= ctrlCurve + 'offset')
        cmds.group(ctrlCurve + 'offset', n=ctrlCurve + 'grp')
        cmds.parent(buildCurve, ctrlCurve + 'offset')
        cmds.connectAttr(buildCurve + '.worldSpace[0]', ctrlCurve + '.create', f=True)

        i = 0

        for ctrl in ctrlList :
            cmds.select(clear=True)

            cmds.curve(d=1, p=diamond)
            cmds.rename('curve1', ctrl)
            cmds.group(ctrl, n=ctrl + '_offset')
            cmds.group(ctrl + '_offset', n=ctrl + '_grp')

            cmds.connectAttr(ctrlCurve + '.editPoints[' + str(i) + ']', ctrl + '_grp.translate')
            if i == 7 :
                cmds.connectAttr(ctrl + '.translate', ctrlCurve + '.cv[' + str(0) + ']')
            else :
                cmds.connectAttr(ctrl + '.translate', ctrlCurve + '.cv[' + str(i+1) + ']')
            cmds.createNode('multiplyDivide', n=ctrl + '_MD')
            cmds.setAttr(ctrl + '_MD.input2X', -1)
            cmds.setAttr(ctrl + '_MD.input2Y', -1)
            cmds.setAttr(ctrl + '_MD.input2Z', -1)
            cmds.connectAttr(ctrl + '.translate', ctrl + '_MD.input1')
            cmds.connectAttr(ctrl + '_MD.output', ctrl + '_offset.translate')
            cmds.parent(ctrl + '_grp', ctrlCurve)

            i += 1

    # widgets

    def createWidget(self):

        self.ribbonNameLineEdit = QtWidgets.QLineEdit("ribbon name")
        self.ribbonNameLineEdit.textChanged.connect(self.ribbonNameLineEdit_func)

        self.edgeLoopCheckbox = QtWidgets.QCheckBox("select edgeLoop")
        self.edgeLoopCheckbox.clicked.connect(self.edgeLoopCheckbox_func)

        self.parentJointCheckbox = QtWidgets.QCheckBox("select parent joint")
        self.parentJointCheckbox.clicked.connect(self.parentJointCheckbox_func)

        self.buildButton = QtWidgets.QPushButton("Build")
        self.buildButton.clicked.connect(self.buildButton_func)

        self.controlGuidesButton = QtWidgets.QPushButton("build guides")
        self.controlGuidesButton.clicked.connect(self.controlGuidesButton_func)

    # layout

    def createLayout(self):
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addWidget(self.ribbonNameLineEdit)
        mainLayout.addWidget(self.edgeLoopCheckbox)
        mainLayout.addWidget(self.parentJointCheckbox)
        mainLayout.addWidget(self.buildButton)
        mainLayout.addWidget(self.controlGuidesButton)

"""d = wireBasedCurveRibbonMakerWin()
d.show()"""