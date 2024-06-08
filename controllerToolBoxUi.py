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


class ControllerToolBoxWin(QtWidgets.QDialog):

    def __init__(self, parent=mayaMainWindow()):
        super(ControllerToolBoxWin, self).__init__(parent)
        self.setWindowTitle("controller toolbox")
        self.setMinimumWidth(200)
        # self.setMinimumHeight(500)
        self.side = None
        self.inv = None
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.createWidget()
        self.createLayout()

        self.colorSliderValue = 0
        self.shapeColor = 0
        self.colorBox = (0, 0, 0)


    # function

    def colorSlider_func(self):
        self.shapeColor = int(self.colorSlider.value())

    def setColorBox_func(self):
        self.colorSliderValue = int(self.colorSlider.value())
        colorValue = int(self.colorSliderValue)

        colorList = cmds.colorIndex(int(colorValue), q=True)
        colorL = []

        for color in colorList:
            color =color*255
            if color == 0:
                color += 1
            colorL.append(color)

        self.colorBox = (int(colorL[0]), int(colorL[1]), int(colorL[2]))
        # print(self.colorBox)

        self.colorVis.setStyleSheet("background-color:rgb" + str(self.colorBox))


    # call function

    def runShapeSwapButton_func(self):
        from plageRigScript import shapeSwapButton

        importlib.reload(shapeSwapButton)

        shapeSwapButton.shapeSwap_func()

    def runChangeShapeSizeButton_func(self):
        from plageRigScript import changeShapeSize

        importlib.reload(changeShapeSize)

        changeShapeSize.shapeSize_func()

    def runChangeShapeColorButton_func(self):
        from plageRigScript import changeShapeColor

        importlib.reload(changeShapeColor)

        changeShapeColor.ShapeColor_func(self.shapeColor)

    def searchForLineEdit_func(self):
        self.side = self.searchForLineEdit.text()

    def replaceByLineEdit_func(self):
        self.inv = self.replaceByLineEdit.text()

    def runMirrorShapeButton_func(self):
        from plageRigScript import mirrorShape

        importlib.reload(mirrorShape)

        mirrorShape.mirrorShape_func(self.side, self.inv)

    # widgets

    def createWidget(self):

        self.runShapeSwapButton = QtWidgets.QPushButton("Change controller shape")
        self.runShapeSwapButton.clicked.connect(self.runShapeSwapButton_func)

        self.runChangeShapeSizeButton = QtWidgets.QPushButton("Change controller size")
        self.runChangeShapeSizeButton.clicked.connect(self.runChangeShapeSizeButton_func)

        self.colorVis = QtWidgets.QPushButton()
        self.colorVis.setStyleSheet("background-color rgb: (0.6079999804496765, 0.0, 0.15700000524520874)")

        self.colorSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.colorSlider.setMinimum(0)
        self.colorSlider.setMaximum(30)
        self.colorSlider.setSingleStep(1)
        self.colorSlider.sliderMoved.connect(self.colorSlider_func)
        self.colorSlider.sliderMoved.connect(self.setColorBox_func)

        self.runChangeShapeColorButton = QtWidgets.QPushButton("Change controller color")
        self.runChangeShapeColorButton.clicked.connect(self.runChangeShapeColorButton_func)

        self.searchForLineEdit = QtWidgets.QLineEdit("search for ?")
        self.searchForLineEdit.textChanged.connect(self.searchForLineEdit_func)

        self.replaceByLineEdit = QtWidgets.QLineEdit("replace by ?")
        self.replaceByLineEdit.textChanged.connect(self.replaceByLineEdit_func)

        self.runMirrorShapeButton = QtWidgets.QPushButton("mirror controller shape")
        self.runMirrorShapeButton.clicked.connect(self.runMirrorShapeButton_func)

    # layout

    def createLayout(self):
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addWidget(self.runShapeSwapButton)
        mainLayout.addWidget(self.runChangeShapeSizeButton)
        mainLayout.addWidget(self.colorSlider)
        mainLayout.addWidget(self.colorVis)
        mainLayout.addWidget(self.runChangeShapeColorButton)
        mainLayout.addWidget(self.searchForLineEdit)
        mainLayout.addWidget(self.replaceByLineEdit)
        mainLayout.addWidget(self.runMirrorShapeButton)

"""d = ControllerToolBoxWin()
d.show()"""