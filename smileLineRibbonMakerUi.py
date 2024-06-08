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


class SmileLineRibbonMakerWin(QtWidgets.QDialog):

    def __init__(self, parent=mayaMainWindow()):
        super(SmileLineRibbonMakerWin, self).__init__(parent)
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
        cmds.polyToCurve(n="smileLine_crv1", form=2, degree=3, conformToSmoothMeshPreview=1)
        cmds.DeleteHistory("smileLine_crv1")
        #cmds.createNode("curveInfo")
        #cmds.rename("curveInfo1", "lips_crv1_curveInfo")
        #cmds.connectAttr("lips_crv1.worldSpace[0]", "lips_crv1_curveInfo.inputCurve")
        # crv1Length = cmds.getAttr("lips_crv1_curveInfo.arcLength")
        #cmds.delete("lips_crv1_curveInfo")

        cmds.select(clear=True)
        cmds.select(self.edgeloop2)
        cmds.polyToCurve(n="smileLine_crv2_temp", form=2, degree=3, conformToSmoothMeshPreview=1)
        cmds.DeleteHistory("smileLine_crv2_temp")
        #cmds.createNode("curveInfo")
        #cmds.rename("curveInfo1", "lips_crv2_curveInfo")
        #cmds.connectAttr("lips_crv2.worldSpace[0]", "lips_crv2_curveInfo.inputCurve")
        # crv2Length = cmds.getAttr("lips_crv2_curveInfo.arcLength")
        #cmds.delete("lips_crv2_curveInfo")

        # crvLength = (float(crv1Length) + float(crv2Length)) / 2

        cvn = int(jointNumber)
        cmds.duplicate("smileLine_crv1")
        #cmds.rename('lips_crv2', 'lips_crv2_temp')
        cmds.rename('smileLine_crv3', 'smileLine_crv2')
        for cv in range(cvn):

            cvName = 'smileLine_crv2.cv[' + str(cv) + ']'
            cvPos = cmds.xform(cvName, q=True, t=True)
            cv2Name = 'smileLine_crv2_temp.cv[' + str(cv) + ']'
            cv2Pos = cmds.xform(cv2Name, q=True, t=True)
            cvM = cv2Pos

            cvDist = math.sqrt(((cvPos[0] - cv2Pos[0]) * (cvPos[0] - cv2Pos[0])) + (
                        (cvPos[1] - cv2Pos[1]) * (cvPos[1] - cv2Pos[1])) + (
                                           (cvPos[2] - cv2Pos[2]) * (cvPos[2] - cv2Pos[2])))

            for i in range(cvn):

                cv3Name = 'smileLine_crv2_temp.cv[' + str(i) + ']'
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

        cmds.loft("smileLine_crv1", "smileLine_crv2", n="smileLineBuild_ribbon")
        #cmds.DeleteHistory("lips_ribbon")
        cmds.Duplicate("smileLineBuild_ribbon")
        cmds.rename("smileLineBuild_ribbon1", "smileLine_ribbon")
        cmds.connectAttr("smileLineBuild_ribbon.worldSpace[0]", "smileLine_ribbon.create")

        cmds.select(clear=True)

        # create follicles

        cmds.group(n="follicle_grp", em=True)

        i = 0
        num = 1
        flList = []
        for fl in range(jointNumber):
            follicleShape = "smileLine" + str(num) + "_follicleShape"
            follicle = "smileLine" + str(num) + "_follicle"
            cmds.createNode("follicle", n=follicleShape)
            cmds.setAttr(follicleShape + ".simulationMethod", 0)

            cmds.connectAttr("smileLine_ribbon.worldMatrix", follicleShape + ".inputWorldMatrix", f=True)
            cmds.connectAttr("smileLine_ribbon.local", follicleShape + ".inputSurface", f=True)
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
        if self.edgeloop1:
            print("Select edgeloop")
        else:
            self.edgeloop1 = cmds.ls(sl=True)
            print(self.edgeloop1)

    def edgeLoop2Checkbox_func(self):
        if self.edgeloop2:
            print("Select edgeloop")
        else:
            self.edgeloop2 = cmds.ls(sl=True)
            print(self.edgeloop2)

    def importLocButton_func(self):

        locList = ['noseCorner_loc',
                   'smileWrinkle_loc',
                   'smileLineCorner_loc',
                   'frownWrinkle_loc',
                   'jawWrinkle_loc']
        locPos = [[-2.5193065652015445, 8.344053470186957, 0.0],
                  [-5.566023854740018, 6.508685930139341, 0.0],
                  [-6.518881747044043, 3.888949619227393, 0.0],
                  [-3.6171918965463226, 1.5483544070745934, 0.0],
                  [0.0, 0.0, 0.0]]
        n = 0

        if cmds.objExists('smileLine_guides'):
            ok = 1
        else:
            cmds.group(n='smileLine_guides', em=True)

        for loc in locList:
            if cmds.objExists(loc):
                cmds.delete(loc)

            cmds.spaceLocator(n=loc)
            cmds.xform(loc, t=locPos[n])
            cmds.parent(loc, 'smileLine_guides')

            n += 1

    def buildControlButton_func(self):

        if cmds.objExists('noseCorner_loc') :
            cmds.select(clear=True)

            locList = ['noseCorner_loc',
                   'smileWrinkle_loc',
                   'smileLineCorner_loc',
                   'frownWrinkle_loc',
                   'jawWrinkle_loc']

            cmds.group(em=True, n="smileLine_ctrl_grp")
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

                cmds.parent(ctrlName + "_grp", "smileLine_ctrl_grp")
        else:
            print("import control marker first")

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