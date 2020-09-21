import maya.cmds as cmds
import maya.OpenMaya as om
import FK_IK_Blend
import Functions
import AutoFK
import AutoIK
#-------------------------------------------------------------------
def Rig_Quick_Menue():
    window_name = "Anas_Rig_Menue"
    cmds.window(title=window_name, iconName="winTest", height=300, width=300)
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    window = cmds.window(window_name)
    scroll = cmds.scrollLayout(verticalScrollBarAlwaysVisible=True)
    cmds.showWindow(window)
#-------------------------------------------------------------------
def gui_layout():
    cmds.columnLayout(adjustableColumn=True)
    cmds.rowColumnLayout()
    cmds.columnLayout()
    cmds.button(l='Default_CTRL', c='defControl()', h=40, w=300)
    cmds.button(l='ParentShape', c="cmds.parent(r=1, s=1)", h=40, w=300)
    cmds.button(l='DelConst', c='deleteConst()', h=40, w=300)
    cmds.rowColumnLayout()
    cmds.columnLayout()
    cmds.frameLayout("Recall_Custom_CTRL")
    cmds.textField("name", insertText="")
    cmds.frameLayout("Choose Constraint For FK_Chain")
    cmds.radioCollection("Constraint_Type")
    cmds.radioButton("Parent")
    cmds.radioButton("Orient")
    cmds.button(l='Auto_FK', c='AutoFK.auto_fk()', h=65, w=300)
    cmds.button(l='Auto_IK', c='AutoIK.auto_ik()', h=65, w=300)
    cmds.button(l='FK/IK_Blend', c='FK_IK_Blend.fk_ik_blend()', h=65, w=300)
    cmds.button(l='Match/Align', c='matcher()', h=50, w=300)
    cmds.button(l='Make_REF', c='make_ref()', h=30, w=300)
    cmds.button(l='Make_Normal', c='return_normal()', h=30, w=300)
    cmds.rowColumnLayout()
    cmds.columnLayout()
    cmds.button(l='Parent/MO=1', c='cmds.parentConstraint(mo=1)', h=30, w=300)
    cmds.button(l='Orient/MO=1', c="cmds.orientConstraint(mo=1)", h=30, w=300)
    cmds.button(l='Point/MO=1', c="cmds.pointConstraint(mo=1)", h=30, w=300)
#-------------------------------------------------------------------
Rig_Quick_Menue()
gui_layout()
#------------------------------------------------------------------
