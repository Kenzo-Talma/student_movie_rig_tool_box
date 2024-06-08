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


class poseSetterWin(QtWidgets.QDialog):

    def __init__(self, parent=mayaMainWindow()):
        super(poseSetterWin, self).__init__(parent)
        self.setWindowTitle("poseSetter")
        self.setMinimumWidth(200)
        # self.setMinimumHeight(500)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.groupName = None

        self.createWidget()
        self.createLayout()

    def createDataNode(self, ctrlName):
        n = 1
        if n < 10:
            nodeName = ctrlName + 'poseSetter_data_node_00' + str(n)
        elif 9 < n < 100:
            nodeName = ctrlName + 'poseSetter_data_node_0' + str(n)
        elif 100 < n:
            nodeName = ctrlName + 'poseSetter_data_node_' + str(n)

        while cmds.objExists(nodeName):
            n += 1
            if n < 10:
                nodeName = ctrlName + 'poseSetter_data_node_00' + str(n)
            elif 9 < n < 100:
                nodeName = ctrlName + 'poseSetter_data_node_0' + str(n)
            elif 100 < n:
                nodeName = ctrlName + 'poseSetter_data_node_' + str(n)

        cmds.group(em=True, n=nodeName)

        hidingList = ['.translateX',
                      '.translateY',
                      '.translateZ',
                      '.rotateX',
                      '.rotateY',
                      '.rotateZ',
                      '.scaleX',
                      '.scaleY',
                      '.scaleZ',
                      '.visibility']
        createAttrList = ['origPose_translateX',
                          'origPose_translateY',
                          'origPose_translateZ',
                          'origPose_rotateX',
                          'origPose_rotateY',
                          'origPose_rotateZ',
                          'origPose_scaleX',
                          'origPose_scaleY',
                          'origPose_scaleZ',
                          'animPose_translateX',
                          'animPose_translateY',
                          'animPose_translateZ',
                          'animPose_rotateX',
                          'animPose_rotateY',
                          'animPose_rotateZ',
                          'animPose_scaleX',
                          'animPose_scaleY',
                          'animPose_scaleZ']

        for at in hidingList:
            cmds.setAttr(nodeName + at, lock=True, channelBox=False, keyable=False)

        for at in createAttrList:
            cmds.select(nodeName)
            cmds.addAttr(ln=at, k=True)

        return (nodeName)

    def getPose_func(self):
        ctrlList = cmds.ls(sl=True, type='transform')
        attrList = ['.translateX',
                    '.translateY',
                    '.translateZ',
                    '.rotateX',
                    '.rotateY',
                    '.rotateZ',
                    '.scaleX',
                    '.scaleY',
                    '.scaleZ']
        for ctrl in ctrlList:

            if input('do you want to overwrite data ? (0/1)'):
                if cmds.objExists('poseSetter_data_node_001'):
                    dataNode = ctrl + 'poseSetter_data_node_001'
                else:
                    dataNode = self.createDataNode(ctrl)
            else:
                dataNode = self.createDataNode(ctrl)
                print(dataNode)

            for at in attrList:
                att = cmds.getAttr(ctrl + at)
                cmds.setAttr(dataNode + '.animPose_' + at.split('.')[1], att)

                atto = cmds.getAttr(ctrl + '_grp' + at)
                cmds.setAttr(dataNode + '.origPose_' + at.split('.')[1], atto)

    def setAnimPose_func(self):
        ctrlList = cmds.ls(sl=True, type='transform')
        attrList1 = ['.translateX',
                     '.translateY',
                     '.translateZ',
                     '.rotateX',
                     '.rotateY',
                     '.rotateZ', ]
        attrList2 = ['.scaleX',
                     '.scaleY',
                     '.scaleZ']

        for ctrl in ctrlList:
            dataNode = ctrl + 'poseSetter_data_node_001'
            if cmds.objExists(dataNode) :
                n = 0
                while cmds.objExists(dataNode):
                    if n < 10:
                        dataNode = ctrl + 'poseSetter_data_node_00' + str(n)
                    elif 9 < n < 100:
                        dataNode = ctrl + 'poseSetter_data_node_0' + str(n)
                    elif 100 < n:
                        dataNode = ctrl + 'poseSetter_data_node_' + str(n)
                    n+=1
                if n==1:
                    dataNode = ctrl + 'poseSetter_data_node_001'
            else:
                dataNode = ctrl + 'poseSetter_data_node_001'

            for at in attrList1:
                cmds.setAttr(ctrl + at, 0)

                cmds.setAttr(ctrl + '_grp' + at,
                             cmds.getAttr(dataNode + '.origPose_' + at.split('.')[1]) + cmds.getAttr(dataNode + '.animPose_' + at.split('.')[1]))

            for at in attrList2:
                cmds.setAttr(ctrl + at, 1)

                cmds.setAttr(ctrl + '_grp' + at,
                             cmds.getAttr(dataNode + '.animPose_' + at.split('.')[1]))

    def setOrigPose_func(self):
        ctrlList = cmds.ls(sl=True, type='transform')
        attrList1 = ['.translateX',
                     '.translateY',
                     '.translateZ',
                     '.rotateX',
                     '.rotateY',
                     '.rotateZ', ]
        attrList2 = ['.scaleX',
                     '.scaleY',
                     '.scaleZ']

        for ctrl in ctrlList:
            dataNode = ctrl + 'poseSetter_data_node_001'
            if cmds.objExists(dataNode):
                n = 0
                while cmds.objExists(dataNode):
                    if n < 10:
                        dataNode = ctrl + 'poseSetter_data_node_00' + str(n)
                    elif 9 < n < 100:
                        dataNode = ctrl + 'poseSetter_data_node_0' + str(n)
                    elif 100 < n:
                        dataNode = ctrl + 'poseSetter_data_node_' + str(n)
                    n += 1
                if n == 1:
                    dataNode = ctrl + 'poseSetter_data_node_001'
            else:
                dataNode = ctrl + 'poseSetter_data_node_001'

            for at in attrList1:
                cmds.setAttr(ctrl + at, cmds.getAttr(dataNode + '.animPose_' + at.split('.')[1]))

                cmds.setAttr(ctrl + '_grp' + at, cmds.getAttr(dataNode + '.origPose_' + at.split('.')[1]))

            for at in attrList2:
                cmds.setAttr(ctrl + at, cmds.getAttr(dataNode + '.animPose_' + at.split('.')[1]))

                cmds.setAttr(ctrl + '_grp' + at, cmds.getAttr(dataNode + '.origPose_' + at.split('.')[1]))

    def createWidget(self):

        self.getPoseButton = QtWidgets.QPushButton("get pose")
        self.getPoseButton.clicked.connect(self.getPose_func)

        self.setAnimPoseButton = QtWidgets.QPushButton("set animation pose")
        self.setAnimPoseButton.clicked.connect(self.setAnimPose_func)

        self.setOrigPoseButton = QtWidgets.QPushButton("return to bind pose")
        self.setOrigPoseButton.clicked.connect(self.setOrigPose_func)

    def createLayout(self):
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addWidget(self.getPoseButton)
        mainLayout.addWidget(self.setAnimPoseButton)
        mainLayout.addWidget(self.setOrigPoseButton)