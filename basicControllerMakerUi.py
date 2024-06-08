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


class BasicControllerMakerWin(QtWidgets.QDialog):

    def __init__(self, parent=mayaMainWindow()):
        super(BasicControllerMakerWin, self).__init__(parent)
        self.setWindowTitle("basic controller maker")
        self.setMinimumWidth(200)
        # self.setMinimumHeight(500)
        self.ctrlList = []
        self.side = None
        self.inv = None
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.createWidget()
        self.createLayout()

    # function

    def runCreateLocButton_func(self):
        obList = cmds.ls(sl=True)

        for n, ob in enumerate(obList):
            locName = 'controlMarker_' + str(n+1)
            cmds.spaceLocator(n=locName)

            pos = cmds.xform(ob, q=True, t=True, ws=True, a=True)
            cmds.xform(locName, t=pos, ws=True, a=True)

            n += 1

    def runBuildButton_func(self):
        locList = cmds.ls(sl=True)

        for loc in locList:
            ctrlName = loc + '_ctrl'
            jntName = loc + '_jnt'

            cmds.circle(n=ctrlName)
            cmds.DeleteHistory(ctrlName)
            cmds.group(ctrlName, n=ctrlName + '_offset')
            cmds.group(ctrlName + '_offset', n=ctrlName + '_grp')

            cmds.joint(n=jntName)
            cmds.group(jntName, n=jntName + '_offset')
            cmds.group(jntName + '_offset', n=jntName + '_grp')

            cmds.parent(jntName + '_grp', ctrlName)

            pos = cmds.xform(loc, q=True, t=True)
            rot = cmds.xform(loc, q=True, ro= True)

            cmds.xform(ctrlName + '_grp', t=pos)
            cmds.xform(ctrlName + '_grp', ro=rot)

            self.ctrlList.append(ctrlName + '_grp')

    def searchForLineEdit_func(self):
        self.side = self.searchForLineEdit.text()

    def replaceByLineEdit_func(self):
        self.inv = self.replaceByLineEdit.text()

    def runMirrorButton_func(self):
        side = self.side
        inv = self.inv

        for ctrl in self.ctrlList:
            ctrlPos = cmds.xform(ctrl, q=True, t=True, ws=True, a=True)
            ctrlRot = cmds.xform(ctrl, q=True, ro=True, ws=True, a=True)
            ctrlInv = ctrl.replace(side, inv)
            ctrlPosInv = (-ctrlPos[0], ctrlPos[1], ctrlPos[2])
            ctrlRotInv = (ctrlRot[0], ctrlRot[1] + 180, ctrlRot[2])

            if ctrlPos != 0:
                cmds.duplicate(ctrl)
                cmds.rename(ctrl + '1', ctrlInv)
                cmds.xform(ctrlInv, t=ctrlPosInv, ws=True, a=True)
                cmds.xform(ctrlInv, ro=ctrlRotInv, ws=True, a=True)

            self.ctrlList = []

    # widgets

    def createWidget(self):
            self.runCreateLocButton = QtWidgets.QPushButton("create marker")
            self.runCreateLocButton.clicked.connect(self.runCreateLocButton_func)

            self.runBuildButton = QtWidgets.QPushButton("build controller")
            self.runBuildButton.clicked.connect(self.runBuildButton_func)

            self.searchForLineEdit = QtWidgets.QLineEdit("search for ?")
            self.searchForLineEdit.textChanged.connect(self.searchForLineEdit_func)

            self.replaceByLineEdit = QtWidgets.QLineEdit("replace by ?")
            self.replaceByLineEdit.textChanged.connect(self.replaceByLineEdit_func)

            self.runMirrorButton = QtWidgets.QPushButton("mirror controller")
            self.runMirrorButton.clicked.connect(self.runMirrorButton_func)

    # layout

    def createLayout(self):
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addWidget(self.runCreateLocButton)
        mainLayout.addWidget(self.runBuildButton)
        mainLayout.addWidget(self.searchForLineEdit)
        mainLayout.addWidget(self.replaceByLineEdit)
        mainLayout.addWidget(self.runMirrorButton)