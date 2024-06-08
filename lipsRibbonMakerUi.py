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


class LipsRibbonMakerWin(QtWidgets.QDialog):

    def __init__(self, parent=mayaMainWindow()):
        super(LipsRibbonMakerWin, self).__init__(parent)
        self.edgeloop1 = None
        self.edgeloop2 = None
        self.parentJnt = None
        self.setWindowTitle("Ribbon maker")
        self.setMinimumWidth(200)
        # self.setMinimumHeight(500)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.createWidget()
        self.createLayout()

    # get edgeLoop Functions

    def buildButton_func(self):
        jointNumber = 0

        for ob in self.edgeloop1:
            jointNumber += 1
        print(jointNumber)

        cmds.select(clear=True)
        cmds.select(self.edgeloop1)
        cmds.polyToCurve(n="lips_crv1", form=2, degree=3, conformToSmoothMeshPreview=1)
        cmds.DeleteHistory("lips_crv1")
        #cmds.createNode("curveInfo")
        #cmds.rename("curveInfo1", "lips_crv1_curveInfo")
        #cmds.connectAttr("lips_crv1.worldSpace[0]", "lips_crv1_curveInfo.inputCurve")
        # crv1Length = cmds.getAttr("lips_crv1_curveInfo.arcLength")
        #cmds.delete("lips_crv1_curveInfo")

        cmds.select(clear=True)
        cmds.select(self.edgeloop2)
        cmds.polyToCurve(n="lips_crv2_temp", form=2, degree=3, conformToSmoothMeshPreview=1)
        cmds.DeleteHistory("lips_crv2_temp")
        #cmds.createNode("curveInfo")
        #cmds.rename("curveInfo1", "lips_crv2_curveInfo")
        #cmds.connectAttr("lips_crv2.worldSpace[0]", "lips_crv2_curveInfo.inputCurve")
        # crv2Length = cmds.getAttr("lips_crv2_curveInfo.arcLength")
        #cmds.delete("lips_crv2_curveInfo")

        # crvLength = (float(crv1Length) + float(crv2Length)) / 2

        cvn = int(jointNumber)
        cmds.duplicate("lips_crv1")
        #cmds.rename('lips_crv2', 'lips_crv2_temp')
        cmds.rename('lips_crv3', 'lips_crv2')
        for cv in range(cvn):

            cvName = 'lips_crv2.cv[' + str(cv) + ']'
            cvPos = cmds.xform(cvName, q=True, t=True)
            cv2Name = 'lips_crv2_temp.cv[' + str(cv) + ']'
            cv2Pos = cmds.xform(cv2Name, q=True, t=True)
            cvM = cv2Pos

            cvDist = math.sqrt(((cvPos[0] - cv2Pos[0]) * (cvPos[0] - cv2Pos[0])) + (
                        (cvPos[1] - cv2Pos[1]) * (cvPos[1] - cv2Pos[1])) + (
                                           (cvPos[2] - cv2Pos[2]) * (cvPos[2] - cv2Pos[2])))

            for i in range(cvn):

                cv3Name = 'lips_crv2_temp.cv[' + str(i) + ']'
                cv3Pos = cmds.xform(cv3Name, q=True, t=True)
                cvTestDist = math.sqrt(((cvPos[0] - cv3Pos[0]) * (cvPos[0] - cv3Pos[0])) + (
                            (cvPos[1] - cv3Pos[1]) * (cvPos[1] - cv3Pos[1])) + (
                                                   (cvPos[2] - cv3Pos[2]) * (cvPos[2] - cv3Pos[2])))
                if cvDist > cvTestDist:
                    cvDist = cvTestDist
                    cvM = cv3Pos
                else:
                    aaaaaaaaaa = 1

            cmds.xform(cvName, t=cvM)

        cmds.loft("lips_crv1", "lips_crv2", n="lipsBuild_ribbon")
        #cmds.DeleteHistory("lips_ribbon")
        cmds.Duplicate("lipsBuild_ribbon")
        cmds.rename("lipsBuild_ribbon1", "lips_ribbon")
        cmds.connectAttr("lipsBuild_ribbon.worldSpace[0]", "lips_ribbon.create")

        cmds.select(clear=True)

        # create follicles

        cmds.group(n="follicle_grp", em=True)

        i = 0
        num = 1
        flList = []
        for fl in range(jointNumber):
            follicleShape = "lips" + str(num) + "_follicleShape"
            follicle = "lips" + str(num) + "_follicle"
            cmds.createNode("follicle", n=follicleShape)
            cmds.setAttr(follicleShape + ".simulationMethod", 0)

            cmds.connectAttr("lips_ribbon.worldMatrix", follicleShape + ".inputWorldMatrix", f=True)
            cmds.connectAttr("lips_ribbon.local", follicleShape + ".inputSurface", f=True)
            cmds.connectAttr(follicleShape + ".outRotate", follicle + ".rotate", f=True)
            cmds.connectAttr(follicleShape + ".outTranslate", follicle + ".translate", f=True)

            V = ((1 / float(jointNumber)) * float(i))

            cmds.setAttr(follicleShape + ".parameterU", 0.5)
            cmds.setAttr(follicleShape + ".parameterV", V)

            cmds.parent(follicle, "follicle_grp")
            i += 1
            num += 1
            flList.append(follicle)

        # create joint

        for fl in flList:
            jnt = fl.split("_f")[0] + "_jnt"

            cmds.select(clear=True)

            cmds.joint(n=jnt)
            cmds.parent(jnt, fl)
            cmds.xform(jnt, t=(0, 0, 0))
            cmds.xform(jnt, ro=(0, 0, 0))
            cmds.setAttr(jnt + ".jointOrientX", 0)
            cmds.setAttr(jnt + ".jointOrientY", 0)
            cmds.setAttr(jnt + ".jointOrientZ", 0)

    def edgeLoop1Checkbox_func(self):
        self.edgeloop1 = cmds.ls(sl=True)
        #print(self.edgeloop1)

    def edgeLoop2Checkbox_func(self):
        self.edgeloop2 = cmds.ls(sl=True)
        #print(self.edgeloop2)

    def parentJntCheckbox_func(self):

        self.parentJnt = cmds.ls(sl=True, type= 'joint')

        if self.parentJnt:
            print('select head joint')

    def parentJntButton_func(self):
        jntList = cmds.ls(sl=True, type='joint')

        for jnt in jntList:
            cmds.rename(jnt, 'SKIN_' + jnt)
            cmds.duplicate('SKIN_' + jnt, n=jnt)
            cmds.parent('SKIN_' + jnt, 'SKIN_grp')
            cmds.xform('SKIN_' + jnt, t=(0, 0, 0))
            cmds.xform('SKIN_' + jnt, ro=(0, 0, 0))
            cmds.setAttr(jnt + '.inheritsTransform', 0)
            cmds.connectAttr(jnt + '.worldMatrix', 'SKIN_' + jnt + '.offsetParentMatrix')

            cmds.setAttr('SKIN_' + jnt + '.jointOrientX', 0)
            cmds.setAttr('SKIN_' + jnt + '.jointOrientY', 0)
            cmds.setAttr('SKIN_' + jnt + '.jointOrientZ', 0)

    def importLocButton_func(self):

        cmds.file("Y:\E5\plage\library\RIG_lib\kRibbon\kLips_Ribbon_ctrl_guides.ma", i=True, f=True)

    def buildControlButton_func(self):

        if cmds.objExists("M_upperLips_loc") :
            cmds.select(clear=True)

            locList = ["M_upperLips_loc", "R_cornerLips_loc", "R_lowerCornerLips_loc", "R_lowerLips_loc",
                       "M_lowerLips_Loc", "R_upperCornerLips_loc", "R_upperLips_loc"]

            cmds.group(em=True, n="lips_ctrl_grp")
            for loc in locList:
                ctrlName = loc.split("_loc")[0] + "_ctrl"
                jntName = loc.split("_loc")[0] + "_jnt"

                cmds.circle(n=ctrlName)
                cmds.group(ctrlName, n=ctrlName + "_offset")
                cmds.group(ctrlName + "_offset", n=ctrlName + "_grp")

                cmds.joint(n=jntName, rad=3)
                cmds.group(jntName, n=jntName + "_offset")
                cmds.group(jntName + "_offset", n=jntName + "_grp")

                cmds.parent(jntName + "_grp", ctrlName)

                trans = cmds.xform(loc, q=True, t=True, ws=True, a=True)
                rot = cmds.xform(loc, q=True, ro=True, ws=True, a=True)
                cmds.xform(ctrlName + "_grp", t=trans, ws=True, a=True)
                cmds.xform(ctrlName + "_grp", ro=rot, ws=True, a=True)

                cmds.parent(ctrlName + "_grp", "lips_ctrl_grp")
        else:
            print("import control marker first")

    def shapeSwapButton_func(self):
        obList = cmds.ls(sl=True)

        ind = 0

        for ob in obList:
            if ind == 0:
                childrens = cmds.listRelatives(ob, children=True, s=True)
                cmds.delete(childrens)

            else:
                obSh = cmds.listRelatives(ob, children=True, s=True)
                cmds.parent(obSh, obList[0], s=True, r=True)
                cmds.delete(ob)
            ind += 1
        cmds.select(obList[0])
        print("Shape swap done")

    # widgets

    def createWidget(self):
        # self.lineEdit = QtWidgets.QLineEdit()
        self.edgeLoop1Checkbox = QtWidgets.QCheckBox("1st edgeLoop")
        self.edgeLoop1Checkbox.clicked.connect(self.edgeLoop1Checkbox_func)

        self.edgeLoop2Checkbox = QtWidgets.QCheckBox("2nd edgeLoop")
        self.edgeLoop2Checkbox.clicked.connect(self.edgeLoop2Checkbox_func)

        self.buildButton = QtWidgets.QPushButton("Build")
        self.buildButton.clicked.connect(self.buildButton_func)

        """self.parentJntCheckbox = QtWidgets.QCheckBox("select head joint")
        self.parentJntCheckbox.clicked.connect(self.parentJntCheckbox_func)

        self.parentJntButton = QtWidgets.QPushButton("parent lips joints to head")
        self.parentJntButton.clicked.connect(self.parentJntButton_func)"""

        self.importLocButton = QtWidgets.QPushButton("controls marker")
        self.importLocButton.clicked.connect(self.importLocButton_func)

        self.buildControlButton = QtWidgets.QPushButton("Build controllers")
        self.buildControlButton.clicked.connect(self.buildControlButton_func)

        self.shapeSwapButton = QtWidgets.QPushButton("Change controller shape")
        self.shapeSwapButton.clicked.connect(self.shapeSwapButton_func)

    # layout

    def createLayout(self):
        mainLayout = QtWidgets.QVBoxLayout(self)
        # mainLayout.addWidget(self.lineEdit)
        mainLayout.addWidget(self.edgeLoop1Checkbox)
        mainLayout.addWidget(self.edgeLoop2Checkbox)
        mainLayout.addWidget(self.buildButton)
        #mainLayout.addWidget(self.parentJntCheckbox)
        #mainLayout.addWidget(self.parentJntButton)
        mainLayout.addWidget(self.importLocButton)
        mainLayout.addWidget(self.buildControlButton)
        #mainLayout.addWidget(self.shapeSwapButton)

"""if __name__ == "__main__":
    d = LipsRibbonMakerWin()
    d.show()"""