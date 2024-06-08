from student_movie_rig_tool_box import plageRigMainUi
import importlib

importlib.reload(plageRigMainUi)

win = plageRigMainUi.PlageRigMainWin()
win.show()
