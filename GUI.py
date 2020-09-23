import maya.cmds as cmds
import maya.OpenMaya as om
import Auto_FK_IK_Blending
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
    # scroll = cmds.scrollLayout(verticalScrollBarAlwaysVisible=True)
    cmds.showWindow(window)
#-------------------------------------------------------------------
def gui_layout():
    cmds.columnLayout(adjustableColumn=True)
    cmds.rowColumnLayout()
    cmds.columnLayout()
    cmds.frameLayout("Recall_Custom_CTRL")
    cmds.textField("name", insertText="")
    cmds.frameLayout("Choose Constraint For FK_Chain")
    cmds.radioCollection("Constraint_Type")
    cmds.radioButton("Parent")
    cmds.radioButton("Orient")
    cmds.rowColumnLayout(nc=2)
    cmds.button(l='Auto_FK', c='AutoFK.auto_fk()', h=65, w=150)
    cmds.button(l='Auto_IK', c='AutoIK.auto_ik()', h=65, w=150)
    # cmds.button(l='FK/IK_Blend', c='fk_ik_blend()', h=65, w=150)
    cmds.button(label="Main_Joint_List", command="main()", w=150, h=50)
    cmds.button(label="FK/IK_Blend", command="fk_ik_blend()", w=150, h=50)
    cmds.button(label="FK_Joint_List", command="fk()", w=150, h=50)
    cmds.button(label="IK_Joint_List", command="ik()", w=150, h=50)
    cmds.button(l='Match/Align', c='matcher()', h=50, w=150)
    cmds.button(l='Make_REF', c='make_ref()', h=30, w=150)
    cmds.button(l='Make_Normal', c='return_normal()', h=30, w=150)
    cmds.button(l='Default_CTRL', c='defControl()', h=40, w=150)
    cmds.button(l='ParentShape', c="cmds.parent(r=1, s=1)", h=40, w=150)
    cmds.button(l='DelConst', c='deleteConst()', h=40, w=150)
    cmds.button(l='Parent/MO=1', c='cmds.parentConstraint(mo=1)', h=30, w=150)
    cmds.button(l='Orient/MO=1', c="cmds.orientConstraint(mo=1)", h=30, w=150)
    cmds.button(l='Point/MO=1', c="cmds.pointConstraint(mo=1)", h=30, w=150)
#-------------------------------------------------------------------
Rig_Quick_Menue()
gui_layout()
#------------------------------------------------------------------
import sys
import maya.cmds as cmds
#---------------------------------------------------------

