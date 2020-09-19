import maya.OpenMaya as om
import maya.cmds as cmds
#---------------------------------------------------------
# Create Space Locator Function
def create_loc(par):
    loc = cmds.spaceLocator()
    cmds.move(par.x, par.y, par.z, loc[0])
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
    for i in selection:cmds.joint(e=True, spa=True, ch=True)
    # Create IK Handle Between Shoulder And Wrist
    cmds.ikHandle(sj=selection[0], ee=selection[2],name=ik_handle, solver="ikRPsolver")
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
        polevectr_ctrl = cmds.circle(name="polevectr_ctrl", normal=(0, 1, 0), radius=2)[0]
    else:
        polevectr_ctrl = cmds.duplicate(polevectr_ctrl, name="polevectr_ctrl")[0]
    #---------------------------------------------------------
    if ik_ctrl == None or cmds.objExists(ik_ctrl) == False:
        ik_ctrl = cmds.circle(name="ik_arm_ctrl",normal=(0, 1, 0), radius=2)[0]
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
#---------------------------------------------------------
if __init__ == "main":
    auto_ik()