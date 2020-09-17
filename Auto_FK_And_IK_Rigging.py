import maya.cmds as cmds
import maya.OpenMaya as om
#-------------------------------------------------------------------
# Auto_FK_Functions
def auto_fk(*args):
    ctrl = cmds.textField("name", query=True, text=True)
    has_parent = None
    selection = cmds.ls(sl=True)
    radio = cmds.radioCollection("Constraint_Type", query=True, select=True)
    mode = cmds.radioButton(radio, query=True, label=True)

    for i in selection:
        grp = cmds.group(em=True, name="{}_ctrl_grp".format(i))
        # if ctrl is not exist in the scene already
        if ctrl == None or cmds.objExists(ctrl) == False:
            ctrl = cmds.circle(name="{}_ctrl".format(
                i), normal=(0, 1, 0), radius=2)[0]
        else:
            # duplicate it and rename it
            ctrl = cmds.duplicate(ctrl, name="{}_ctrl".format(i))[0]
        loc_name = "{}_ctrl_loc".format(i)
        loc = cmds.CreateLocator()
        cmds.rename(loc, loc_name)
        pc_grp = cmds.parentConstraint(i, grp, mo=0)
        cmds.delete(pc_grp)
        pc_ctrl = cmds.parentConstraint(i, ctrl, mo=0)
        cmds.delete(pc_ctrl)
        pc_loc = cmds.parentConstraint(i, loc_name, mo=0)
        cmds.delete(pc_loc)
        cmds.parent(loc_name, grp)
        cmds.parent(ctrl, loc_name)
        cmds.DeleteHistory(ctrl)
        if i is not None:
            if mode == "Parent":
                cmds.parentConstraint(
                    ctrl, i, mo=1, name="{}_parentConst".format(i))
            elif mode == "Orient":
                cmds.orientConstraint(
                    ctrl, i, mo=1, name="{}_orientConst".format(i))
        if has_parent is not None:
            cmds.parent(grp, has_parent)
        has_parent = ctrl
#-------------------------------------------------------------------
# Create Space Locator Function
def create_loc(vect):
    loc = cmds.spaceLocator()
    cmds.move(vect.x, vect.y, vect.z, loc[0])
    cmds.rename(loc, "Vector_loc_0")
# Auto_IK_And_PoleVector_Function
def auto_ik(*args):
    polevectr_ctrl = cmds.textField("name", query=True, text=True)
    # polevectr_ctrl = None
    ik_ctrl = cmds.textField("name", query=True, text=True)
    # ik_ctrl = None
    polevect_loc = "PoleVector_locator"
    ik_handle = "arm_ik_handle"
    #---------------------------------------------------------
    selection = cmds.ls(sl=True)
    # Set Prefered Angle To The Joints
    for i in selection:
        cmds.joint(e=True, spa=True, ch=True)
    # Create IK Handle Between Shoulder And Wrist
    cmds.ikHandle(sj=selection[0], ee=selection[2],
                  name=ik_handle, solver="ikRPsolver")
    #---------------------------------------------------------
    # Make Shoulder Vector
    shldr_p = cmds.select(selection[0])
    shldr_p = cmds.xform(q=True, ws=True, t=True)
    shldr_vct = om.MVector(shldr_p[0], shldr_p[1], shldr_p[2])
    # Make Elbow Vector
    elbw_p = cmds.select(selection[1])
    elbw_p = cmds.xform(q=True, ws=True, t=True)
    elbw_vct = om.MVector(elbw_p[0], elbw_p[1], elbw_p[2])
    # Make Wrist Vector
    wrst_p = cmds.select(selection[2])
    wrst_p = cmds.xform(q=True, ws=True, t=True)
    wrst_vct = om.MVector(wrst_p[0], wrst_p[1], wrst_p[2])
    #---------------------------------------------------------
    # Get The Distance Between Shoulder And Wrist
    Shldr_wrst_Distance = wrst_vct - shldr_vct
    create_loc(Shldr_wrst_Distance)
    # To Get The Half Distance In Space
    half_distance = Shldr_wrst_Distance * 0.5
    create_loc(half_distance)
    # Get The Half Distance Vector Between Shoulder And Wrist On The Same Line
    half_shldr_wrst = half_distance + shldr_vct
    create_loc(half_shldr_wrst)
    # Get Distance Between The Elbow Joint And The Shoulder/Wrist Half Distance
    elbw_half_distance = elbw_vct - half_shldr_wrst
    create_loc(elbw_half_distance)
    # Double The Distance To Make Pole_Vector Away From The Elbow Joint
    double_distance = elbw_half_distance * 2
    create_loc(double_distance)
    # Get The Pole Vector Location
    pole_vector = double_distance + elbw_vct
    loc = cmds.spaceLocator(name=polevect_loc)
    cmds.move(pole_vector.x, pole_vector.y, pole_vector.z, loc[0])
    #---------------------------------------------------------
    if polevectr_ctrl == None or cmds.objExists(polevectr_ctrl) == False:
        polevectr_ctrl = cmds.circle(
            name="polevectr_ctrl", normal=(0, 1, 0), radius=2)[0]
    else:
        polevectr_ctrl = cmds.duplicate(
            polevectr_ctrl, name="polevectr_ctrl")[0]
    #---------------------------------------------------------
    if ik_ctrl == None or cmds.objExists(ik_ctrl) == False:
        ik_ctrl = cmds.circle(name="ik_arm_ctrl",
                              normal=(0, 1, 0), radius=2)[0]
    else:
        ik_ctrl = cmds.duplicate(ik_ctrl, name="ik_arm_ctrl")[0]
    grp = cmds.group(em=True, name="{}_Grp".format(ik_ctrl))
    cmds.parent(ik_ctrl, grp)
    #---------------------------------------------------------
    pv_grp = cmds.group(em=True, name="{}_Grp".format(polevectr_ctrl))
    cmds.parent(polevectr_ctrl, pv_grp)
    pc = cmds.parentConstraint(polevect_loc, pv_grp, mo=0)
    cmds.delete(pc)
    cmds.poleVectorConstraint(polevectr_ctrl, ik_handle)
    #---------------------------------------------------------
    pcc = cmds.parentConstraint(selection[2], grp, mo=0)
    cmds.delete(pcc)
    cmds.pointConstraint(ik_ctrl, ik_handle)
    cmds.orientConstraint(ik_ctrl, selection[2])
#-------------------------------------------------------------------
def matcher():
    pc = cmds.parentConstraint(mo=0)
    cmds.delete(pc)
#-------------------------------------------------------------------
def deleteConst():
    selection = cmds.ls(sl=True)
    for i in selection:
        cmds.DeleteConstraints()
#-------------------------------------------------------------------
def defControl():
    grp = cmds.group(em=True, name="_ctrl_grp")
    ctrl = cmds.circle(name="_ctrl")
    loc_name = "_CTRL_LOC"
    loc = cmds.CreateLocator()
    cmds.rename(loc, loc_name)
    cmds.parent(ctrl, loc_name)
    cmds.parent(loc_name, grp)
    cmds.DeleteHistory(ctrl)
#-------------------------------------------------------------------
def make_ref():
    selection = cmds.ls(sl=True)
    for i in selection:
        cmds.setAttr("{}.overrideEnabled".format(i), 1)
        cmds.setAttr("{}.overrideDisplayType".format(i), 2)
#-------------------------------------------------------------------
def Rig_Quick_Menue():
    window_name = "Anas_Rig_ITI"
    cmds.window(title=window_name, iconName="winTest", height=300, width=300)
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    window = cmds.window(window_name)
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
    cmds.button(l='Auto_FK', c='auto_fk()', h=80, w=300)
    cmds.button(l='Auto_IK', c='auto_ik()', h=80, w=300)
    cmds.button(l='Match/Align', c='matcher()', h=50, w=300)
    cmds.button(l='Make_REF', c='make_ref()', h=50, w=300)
    cmds.rowColumnLayout()
    cmds.columnLayout()
    cmds.button(l='Parent/MO=1', c='cmds.parentConstraint(mo=1)', h=30, w=300)
    cmds.button(l='Orient/MO=1', c="cmds.orientConstraint(mo=1)", h=30, w=300)
    cmds.button(l='Point/MO=1', c="cmds.pointConstraint(mo=1)", h=30, w=300)
#-------------------------------------------------------------------
Rig_Quick_Menue()
gui_layout()
#------------------------------------------------------------------
