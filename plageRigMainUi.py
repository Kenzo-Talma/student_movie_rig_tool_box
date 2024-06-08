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


class PlageRigMainWin(QtWidgets.QDialog):

    def __init__(self, parent=mayaMainWindow()):
        super(PlageRigMainWin, self).__init__(parent)
        self.setWindowTitle("le rig a la plage")
        self.setMinimumWidth(200)
        # self.setMinimumHeight(500)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.createWidget()
        self.createLayout()

    # functions


    def runControllerToolBoxButton_func(self):
        from student_movie_rig_tool_box import controllerToolBoxUi

        importlib.reload(controllerToolBoxUi)

        controllerToolBoxWin = controllerToolBoxUi.ControllerToolBoxWin()
        controllerToolBoxWin.show()


    def runMakeSkinJointUi_func(self):
        from student_movie_rig_tool_box import makeSkinJointsUi

        importlib.reload(makeSkinJointsUi)

        makeSkinJointsUi.makeSkinJointButton_func()

    def runRibbonMakerButton_func(self):
        from student_movie_rig_tool_box import ribbonMainUi

        importlib.reload(ribbonMainUi)

        ribbonMainUiWin = ribbonMainUi.RibbonMainWin()
        ribbonMainUiWin.show()


    def runBasicControllerMakerButton_func(self):
        from student_movie_rig_tool_box import basicControllerMakerUi

        importlib.reload(basicControllerMakerUi)

        basicControllerMakerWin = basicControllerMakerUi.BasicControllerMakerWin()
        basicControllerMakerWin.show()


    def runPoseInterpollatorConnectButton_func(self):
        from student_movie_rig_tool_box import poseInterpolatorConnect

        importlib.reload(poseInterpolatorConnect)

        poseInterpolatorConnect.poseInterpollatorConnect()


    def runFolloGroupButton_func(self):
        from student_movie_rig_tool_box import followGroupUi

        importlib.reload(followGroupUi)

        followGroupWin = followGroupUi.followGroupWin()
        followGroupWin.show()


    def runKTemplateObjButton_func(self):
        from student_movie_rig_tool_box import kTemplateObj

        importlib.reload(kTemplateObj)

        kTemplateObj.kTemplateObj_func()


    def runKRefObjButton_func(self):
        from student_movie_rig_tool_box import kRefObj

        importlib.reload(kRefObj)

        kRefObj.kRefObj_func()


    def rigAnimPoseSetterUiButton_func(self):
        from student_movie_rig_tool_box import rigAnimPoseSetterUi

        importlib.reload(rigAnimPoseSetterUi)

        followGroupWin = rigAnimPoseSetterUi.poseSetterWin()
        followGroupWin.show()


    def createWidget(self):

        self.runControllerToolBoxButton = QtWidgets.QPushButton("controller tool box")
        self.runControllerToolBoxButton.clicked.connect(self.runControllerToolBoxButton_func)

        self.runMakeSkinJointUiButton = QtWidgets.QPushButton("make skin joint")
        self.runMakeSkinJointUiButton.clicked.connect(self.runMakeSkinJointUi_func)

        self.runKTemplateObjButton = QtWidgets.QPushButton("template selected object")
        self.runKTemplateObjButton.clicked.connect(self.runKTemplateObjButton_func)

        self.runKRefObjButton = QtWidgets.QPushButton("reference selected object")
        self.runKRefObjButton.clicked.connect(self.runKRefObjButton_func)

        self.runFolloGroupButton = QtWidgets.QPushButton("create follow group")
        self.runFolloGroupButton.clicked.connect(self.runFolloGroupButton_func)

        self.runRibbonMakerButton = QtWidgets.QPushButton("ribbon maker")
        self.runRibbonMakerButton.clicked.connect(self.runRibbonMakerButton_func)

        self.runBasicControllerMakerButton = QtWidgets.QPushButton("create basic controller")
        self.runBasicControllerMakerButton.clicked.connect(self.runBasicControllerMakerButton_func)

        self.runPoseInterpollatorConnectButton = QtWidgets.QPushButton("connect pose interpolator")
        self.runPoseInterpollatorConnectButton.clicked.connect(self.runPoseInterpollatorConnectButton_func)

        self.rigAnimPoseSetterUiButton = QtWidgets.QPushButton("Guy change pose")
        self.rigAnimPoseSetterUiButton.clicked.connect(self.rigAnimPoseSetterUiButton_func)


    # layout


    def createLayout(self):
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addWidget(self.runControllerToolBoxButton)
        mainLayout.addWidget(self.runMakeSkinJointUiButton)
        mainLayout.addWidget(self.runKTemplateObjButton)
        mainLayout.addWidget(self.runKRefObjButton)
        mainLayout.addWidget(self.runFolloGroupButton)
        mainLayout.addWidget(self.runRibbonMakerButton)
        mainLayout.addWidget(self.runBasicControllerMakerButton)
        mainLayout.addWidget(self.runPoseInterpollatorConnectButton)
        mainLayout.addWidget(self.rigAnimPoseSetterUiButton)
