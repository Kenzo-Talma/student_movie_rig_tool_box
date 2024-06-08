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


class followGroupWin(QtWidgets.QDialog):

    def __init__(self, parent=mayaMainWindow()):
        super(followGroupWin, self).__init__(parent)
        self.setWindowTitle(" follow group window")
        self.setMinimumWidth(200)
        # self.setMinimumHeight(500)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.groupName = None

        self.createWidget()
        self.createLayout()

    def followGroupButton_func(self):
        ob = cmds.ls(sl=True)[0]

        name = self.groupName + 'Follow' + ob

        cmds.select(clear=True)

        cmds.group(n=name, em=True)
        cmds.setAttr(name + '.inheritsTransform', 0)
        cmds.connectAttr(ob + '.worldMatrix', name + '.offsetParentMatrix', f=True)

    def groupNameLineEdit_func(self):
        self.groupName = self.groupNameLineEdit.text()

    def createWidget(self):

        self.groupNameLineEdit = QtWidgets.QLineEdit("group name ?")
        self.groupNameLineEdit.textChanged.connect(self.groupNameLineEdit_func)

        self.followGroupButton = QtWidgets.QPushButton("create follow group")
        self.followGroupButton.clicked.connect(self.followGroupButton_func)

    def createLayout(self):
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addWidget(self.groupNameLineEdit)
        mainLayout.addWidget(self.followGroupButton)