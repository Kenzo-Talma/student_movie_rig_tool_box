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


class RibbonMainWin(QtWidgets.QDialog):

    def __init__(self, parent=mayaMainWindow()):
        super(RibbonMainWin, self).__init__(parent)
        self.edgeloop1 = None
        self.edgeloop2 = None
        self.setWindowTitle("Ribbon maker")
        self.setMinimumWidth(200)
        # self.setMinimumHeight(500)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.createWidget()
        self.createLayout()


    def runLipsRibbonMakerButton_func(self):
        from student_movie_rig_tool_box import lipsRibbonMakerUi

        importlib.reload(lipsRibbonMakerUi)

        lipsWin = lipsRibbonMakerUi.LipsRibbonMakerWin()
        lipsWin.show()

    def runEyeRibbonMakerButton_func(self):
        """from student_movie_rig_tool_box import lipsRibbonMakerUi

        importlib.reload(lipsRibbonMakerUi)

        lipsWin = lipsRibbonMakerUi.RibbonMakerWin()
        lipsWin.show()"""
        print("no eye ribbon maker yet")

    def runSmileLineRibbonMakerButton_func(self):
        from student_movie_rig_tool_box import smileLineRibbonMakerUi

        importlib.reload(smileLineRibbonMakerUi)

        smileLineWin = smileLineRibbonMakerUi.SmileLineRibbonMakerWin()
        smileLineWin.show()

    def runRegularRibbonMakerButton_func(self):
        from student_movie_rig_tool_box import regularRibbonMakerUi

        importlib.reload(regularRibbonMakerUi)

        regularWin = regularRibbonMakerUi.regularRibbonMakerWin()
        regularWin.show()
        # print("no member ribbon maker yet")

    def runCurveBasedRibbonMakerButton_func(self):
        from student_movie_rig_tool_box import wireBasedCurveRibbonUi

        importlib.reload(wireBasedCurveRibbonUi)

        regularWin = wireBasedCurveRibbonUi.wireBasedCurveRibbonMakerWin()
        regularWin.show()

    # widgets

    def createWidget(self):

        self.runLipsRibbonMakerButton = QtWidgets.QPushButton("lips ribbon")
        self.runLipsRibbonMakerButton.clicked.connect(self.runLipsRibbonMakerButton_func)

        self.runEyeRibbonMakerButton = QtWidgets.QPushButton("lips ribbon")
        self.runEyeRibbonMakerButton.clicked.connect(self.runEyeRibbonMakerButton_func)

        self.runRegularRibbonMakerButton = QtWidgets.QPushButton(" classic ribbon")
        self.runRegularRibbonMakerButton.clicked.connect(self.runRegularRibbonMakerButton_func)

        self.runSmileLineRibbonMakerButton = QtWidgets.QPushButton("smileLine ribbon")
        self.runSmileLineRibbonMakerButton.clicked.connect(self.runSmileLineRibbonMakerButton_func)

        self.runCurveBasedRibbonMakerButton = QtWidgets.QPushButton("curve based ribbon")
        self.runCurveBasedRibbonMakerButton.clicked.connect(self.runCurveBasedRibbonMakerButton_func)

    def createLayout(self):
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addWidget(self.runLipsRibbonMakerButton)
        mainLayout.addWidget(self.runSmileLineRibbonMakerButton)
        mainLayout.addWidget(self.runCurveBasedRibbonMakerButton)
        mainLayout.addWidget(self.runRegularRibbonMakerButton)
