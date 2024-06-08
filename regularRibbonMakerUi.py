import sys
import maya.cmds as cmds
import maya.OpenMayaUI as mui
from PySide2 import QtGui, QtCore, QtWidgets
import shiboken2
import importlib


def mayaMainWindow():
    mainWindowPtr = mui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return (shiboken2.wrapInstance(int(mainWindowPtr), QtWidgets.QWidget))
    else:
        return (shiboken2.wrapInstance(long(mainWindowPtr), QtWidgets.QWidget))

class regularRibbonMakerWin(QtWidgets.QDialog):

    def __init__(self, parent=mayaMainWindow()):
        super(regularRibbonMakerWin, self).__init__(parent)
        self.startLoc = None
        self.endLoc = None
        self.setWindowTitle("Ribbon maker")
        self.setMinimumWidth(200)
        # self.setMinimumHeight(500)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.jointNumber = 3

        self.createWidget()
        self.createLayout()

    def importMarker_func(self):

        # cmds.file('Y:\E5\plage\library\RIG_lib\kRibbon\generalRibbonMarker.ma', i=True)
        start_loc = cmds.spaceLocator(n='ribbon_start_loc')
        end_loc = cmds.spaceLocator(n='ribbon_end_loc')

        cmds.setAttr(start_loc[0]+'.translateY', 1)
        cmds.setAttr(end_loc[0]+'.translateY', -1)


    def startLoc_func(self):

        startLocName = cmds.ls(sl=True)[0]
        self.startLoc = startLocName

    def endLoc_func(self):

        endLocName = cmds.ls(sl=True)[0]
        self.endLoc = endLocName

    def jointNumber_func(self):

        self.jointNumber = int(self.jointNumberLineEdit.text())


    def ribbonMakerButton_func(self):

        # nurbsplane's creation

        startPos = cmds.xform(self.startLoc, q=True, t=True, ws=True)
        startRot = cmds.xform(self.startLoc, q=True, ro=True, ws=True)
        endPos = cmds.xform(self.endLoc, q=True, t=True, ws=True)
        endRot = cmds.xform(self.endLoc, q=True, ro=True, ws=True)

        cmds.distanceDimension(startPoint=(startPos[0], startPos[1], startPos[2]),
                               endPoint=(endPos[0], endPos[1], endPos[2]))
        len = cmds.getAttr("distanceDimensionShape1.distance")

        jointNumber = self.jointNumber

        cmds.delete("distanceDimension1")

        ribbonName = cmds.nurbsPlane(w=1, lr=len, v=2, u=1, n=self.startLoc+"_Ribbon")[0]

        cmds.rotate(0, -90, 0, ribbonName)
        cmds.select(ribbonName)
        cmds.group(em=True, n="Follicle_grp")



        '''i = 0
        num = 1
        for jnt in range(jointNumber + 1):
            follicleShape = self.startLoc + "_FollicleShape_" + str(num)
            follicle = self.startLoc + "_Follicle_" + str(num)

            cmds.createNode("follicle", n=follicleShape)
            cmds.setAttr(follicleShape + ".simulationMethod", 0)

            cmds.connectAttr(ribbonName + ".worldMatrix", follicleShape + ".inputWorldMatrix", f=True)
            cmds.connectAttr(ribbonName + ".local", follicleShape + ".inputSurface", f=True)
            cmds.connectAttr(follicleShape + ".outRotate", follicle + ".rotate", f=True)
            cmds.connectAttr(follicleShape + ".outTranslate", follicle + ".translate", f=True)

            V = ((1 / float(jointNumber)) * float(i))

            cmds.setAttr(self.startLoc + "_FollicleShape_" + str(num) + ".parameterU", 0.5)
            cmds.setAttr(self.startLoc + "_FollicleShape_" + str(num) + ".parameterV", V)

            cmds.parent(follicle, "Follicle_grp")
            i += 1
            num += 1

        # joints's ceation

        num = 1
        for jnt in range(jointNumber + 1):
            follicle = self.startLoc + "_Follicle_" + str(num)

            jointName = self.startLoc + "_Follicle_" + "joint" + str(num)
            cmds.joint(n=jointName)
            cmds.parent(jointName, follicle, a=True)
            cmds.setAttr(jointName + ".translate", 0, 0, 0)
            cmds.setAttr(jointName + ".rotate", 0, 0, 0)

            num += 1'''

        # controls's creation

        # topctrl

        topName = ribbonName + "_Top_ctrl"
        cmds.joint(n=topName + "jnt")
        cmds.group(em=True, n=topName + "jnt" + "_offset")
        cmds.group(em=True, n=topName + "jnt" + "_grp")
        cmds.circle(n=topName)
        cmds.group(em=True, n=topName + "_offset")
        cmds.group(em=True, n=topName + "_grp")
        cmds.parent(topName + "jnt", topName + "jnt" + "_offset")
        cmds.parent(topName + "jnt" + "_offset", topName + "jnt" + "_grp")
        cmds.parent(topName + "jnt" + "_grp", topName)
        cmds.parent(topName, topName + "_offset")
        cmds.parent(topName + "_offset", topName + "_grp")
        cmds.move(0,(len/2), 0, topName + "_grp",)
        cmds.xform(topName + "jnt", t=(0,0,0))

        # midctrl

        midName = ribbonName + "_Mid_ctrl"
        cmds.joint(n=midName + "jnt")
        cmds.group(em=True, n=midName + "jnt" + "_offset")
        cmds.group(em=True, n=midName + "jnt" + "_grp")
        cmds.circle(n=midName)
        cmds.group(em=True, n=midName + "_offset")
        cmds.group(em=True, n=midName + "_grp")
        cmds.parent(midName + "jnt", midName + "jnt" + "_offset")
        cmds.parent(midName + "jnt" + "_offset", midName + "jnt" + "_grp")
        cmds.parent(midName + "jnt" + "_grp", midName)
        cmds.parent(midName, midName + "_offset")
        cmds.parent(midName + "_offset", midName + "_grp")
        cmds.xform(midName + "jnt", t=(0, 0, 0))

        # Lowctrl

        lowName = ribbonName + "_Low_ctrl"
        cmds.joint(n=lowName + "jnt")
        cmds.group(em=True, n=lowName + "jnt" + "_offset")
        cmds.group(em=True, n=lowName + "jnt" + "_grp")
        cmds.circle(n=lowName)
        cmds.group(em=True, n=lowName + "_offset")
        cmds.group(em=True, n=lowName + "_grp")
        cmds.parent(lowName + "jnt", lowName + "jnt" + "_offset")
        cmds.parent(lowName + "jnt" + "_offset", lowName + "jnt" + "_grp")
        cmds.parent(lowName + "jnt" + "_grp", lowName)
        cmds.parent(lowName, lowName + "_offset")
        cmds.parent(lowName + "_offset", lowName + "_grp")
        cmds.move(0, -(len / 2), 0, lowName + "_grp", )
        cmds.xform(lowName + "jnt", t=(0, 0, 0))

        # parent constraint midctrl

        cmds.parentConstraint(topName + "_grp", lowName + "_grp", midName + "_grp", mo=False)

        # bind skin

        cmds.select(ribbonName, topName + "jnt", midName + "jnt", lowName + "jnt")
        cmds.SmoothBindSkin()

        # place ribbon

        cmds.xform(topName + "_grp", t=startPos)
        cmds.xform(lowName + "_grp", t=endPos)
        cmds.xform(topName + "_grp", ro=startRot)
        cmds.xform(lowName + "_grp", ro=endRot)

        # follicle's creation
        joint_list = []
        ribbon_shape = cmds.listRelatives(ribbonName, s=True, type='nurbsSurface', c=True)[0]
        ribbon_shape_orig =cmds.listRelatives(ribbonName, s=True, type='nurbsSurface', c=True)[1]
        print(ribbon_shape_orig)
        # ribbon_shape_orig = cmds.listRelatives(ribbonName, s=True, type='nurbsSurface', c=True)[1]

        u_increment = 1 / (jointNumber - 1)

        # create UV pin node
        uv_pin = ribbonName + '_uvPin'
        if not cmds.objExists(uv_pin):
            uv_pin = cmds.createNode('uvPin', n=uv_pin)
        cmds.connectAttr(ribbon_shape + '.worldSpace[0]', uv_pin + '.deformedGeometry', f=True)
        cmds.connectAttr(ribbon_shape_orig + '.local', uv_pin + '.originalGeometry', f=True)

        for i in range(jointNumber):
            jnt = f'{ribbonName}_{str(i + 1)}_jnt'
            u_pos = u_increment * i

            # create joint
            if not cmds.objExists(jnt):
                jnt = cmds.createNode('joint', n=jnt)

            # connect joint
            cmds.connectAttr(uv_pin + f'.outputMatrix[{str(i)}]', jnt + '.offsetParentMatrix', f=True)

            # set joint position
            cmds.setAttr(uv_pin + f'.coordinate[{str(i)}].coordinateV', u_pos)
            cmds.setAttr(uv_pin + f'.coordinate[{str(i)}].coordinateU', 0.5)

            # connect joint orient
            cmds.setAttr(jnt + '.jointOrientX', -90)
            cmds.setAttr(jnt + '.jointOrientY', -90)

            # add joint to list
            joint_list.append(jnt)


    def createWidget(self):

        self.runimportMarkerButton = QtWidgets.QPushButton("import marker")
        self.runimportMarkerButton.clicked.connect(self.importMarker_func)

        self.runEndlocGetterButton = QtWidgets.QCheckBox("Get end loc")
        self.runEndlocGetterButton.clicked.connect(self.endLoc_func)

        self.runStartlocGetterButton = QtWidgets.QCheckBox("Get start loc")
        self.runStartlocGetterButton.clicked.connect(self.startLoc_func)

        self.jointNumberLineEdit = QtWidgets.QLineEdit("3")
        self.jointNumberLineEdit.textChanged.connect(self.jointNumber_func)

        self.runRibbonMakerButton = QtWidgets.QPushButton("Ribbon maker")
        self.runRibbonMakerButton.clicked.connect(self.ribbonMakerButton_func)

    def createLayout(self):

        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addWidget(self.runimportMarkerButton)
        mainLayout.addWidget(self.runStartlocGetterButton)
        mainLayout.addWidget(self.runEndlocGetterButton)
        mainLayout.addWidget(self.jointNumberLineEdit)
        mainLayout.addWidget(self.runRibbonMakerButton)


"""win = regularRibbonMakerWin()
win.show()"""