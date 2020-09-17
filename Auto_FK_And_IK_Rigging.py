import sys
import maya.cmds as cmds
import maya.OpenMaya as om
#-------------------------------------------------------------------
def auto_fk(*args):
    ctrl = cmds.textField("name", query=True, text=True)
    has_parent = None
    selection = cmds.ls(sl=True)
    radio = cmds.radioCollection("Constraint_Type", query=True, select=True)
    mode = cmds.radioButton(radio, query=True, label=True)

    for i in selection:
        grp = cmds.group(em=True, name ="{}_ctrl_grp".format(i))
        # law el ctrl none aw name bta3oh m4 mawgod fel scene
        if ctrl == None or cmds.objExists(ctrl)==False:
            ctrl = cmds.circle(name = "{}_ctrl".format(i), normal=(0,1,0), radius=2)[0]
        else:
            # e3mel mnnoh duplicate w sammeha
            ctrl = cmds.duplicate(ctrl, name="{}_ctrl".format(i))[0]
        loc_name = "{}_ctrl_loc".format(i)
        loc = cmds.CreateLocator()
        cmds.rename(loc, loc_name)
        pc_grp= cmds.parentConstraint(i,grp,mo=0)
        cmds.delete(pc_grp)
        pc_ctrl = cmds.parentConstraint(i,ctrl,mo=0)
        cmds.delete(pc_ctrl)
        pc_loc = cmds.parentConstraint(i,loc_name,mo=0)
        cmds.delete(pc_loc)
        cmds.parent(loc_name, grp)
        cmds.parent(ctrl, loc_name)
        cmds.DeleteHistory(ctrl)
        if i is not None:
            if mode == "Parent":
                cmds.parentConstraint(ctrl, i, mo=1, name="{}_parentConst".format(i))
            elif mode == "Orient":
                cmds.orientConstraint(ctrl,i, mo=1, name="{}_orientConst".format(i))
        if has_parent is not None:
            cmds.parent(grp, has_parent)
        has_parent = ctrl
#---------------------------------------------------------
def auto_ik(*args):
    #---------------------------------------------------------
    polevectr_ctrl = cmds.textField("name", query=True, text=True)
    ik_ctrl = cmds.textField("name", query=True, text=True)
    polevect_loc = "PoleVector"
    ik_handle = "arm_ik_handle"
    
    selection = cmds.ls(sl=True)
    cmds.ikHandle(sj=selection[0], ee=selection[2],name = ik_handle, solver = "ikRPsolver")
    
    # Get The Vector Of [A] [Shoulder_Jnt]
    cmds.select(selection[0])
    a_poss = cmds.xform(q=True, ws=True, t=True)
    a = om.MVector(a_poss[0], a_poss[1], a_poss[2])
    
    # Get The Vector Of [B] [Elbow_Jnt]
    cmds.select(selection[1])
    b_poss = cmds.xform(q=True, ws=True, t=True)
    b = om.MVector(b_poss[0], b_poss[1], b_poss[2])
    
    # Get The Vector Of [C] [Wrest_Jnt]
    cmds.select(selection[2])
    c_poss = cmds.xform(q=True, ws=True, t=True)
    c = om.MVector(c_poss[0], c_poss[1], c_poss[2])
    #---------------------------------------------------------
    # (Vector[C] - Vector[A]) To Get Vector[F] [The Vector Between [A] and [C]
    f = c - a
    loc = cmds.spaceLocator(name = "VectorF_Loc")
    cmds.move(f.x, f.y, f.z, loc[0])
    #---------------------------------------------------------
    # The Half Distance Of Vector[F] 
    d = f * 0.5
    loc = cmds.spaceLocator(name = "VectorD_Loc")
    cmds.move(d.x, d.y, d.z, loc[0])
    #---------------------------------------------------------
    # Add [D] To [A]
    # To Get The Half Of The Distance Between [A] and [C] 
    e = d + a 
    loc = cmds.spaceLocator(name = "VectorE_Loc")
    cmds.move(e.x, e.y, e.z, loc[0])
    #---------------------------------------------------------
    # Subtract [B] - [E]
    # To Get The Distance Vector[H] Between [E] and [B]
    h = b - e 
    loc = cmds.spaceLocator(name = "VectorH_Loc")
    cmds.move(h.x, h.y, h.z, loc[0])
    #---------------------------------------------------------
    # Multiply Vector[H] By 2
    # To Get The Distance Of PoleVector 
    g = h * 2 
    loc = cmds.spaceLocator(name = "VectorG_Loc")
    cmds.move(g.x, g.y, g.z, loc[0])
    #---------------------------------------------------------
    # Add Vector[G] To Vector[E]
    # To Get The Real Placement Of The PoleVector
    i = g + e 
    loc = cmds.spaceLocator(name = polevect_loc)
    cmds.move(i.x, i.y, i.z, loc[0])
    #---------------------------------------------------------
    
    if polevectr_ctrl == None or cmds.objExists(polevectr_ctrl)==False:
        polevectr_ctrl = cmds.circle(name = "polevectr_ctrl", normal=(0,1,0), radius=2)[0]
    else : 
        polevectr_ctrl = cmds.duplicate(polevectr_ctrl, name="polevectr_ctrl")[0]
    #---------------------------------------------------------
    if ik_ctrl == None or cmds.objExists(ik_ctrl)==False:
        ik_ctrl = cmds.circle(name = "ik_arm_ctrl", normal=(0,1,0), radius=2)[0]
    else : 
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
    ctrl = cmds.circle(name = "_ctrl")
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
        cmds.setAttr("{}.overrideEnabled".format(i),1)
        cmds.setAttr("{}.overrideDisplayType".format(i),2)
#-------------------------------------------------------------------
def Rig_Quick_Menue():
    window_name = "Rig_ITI"
    cmds.window(title = window_name,iconName="winTest", height = 300,width = 300)
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    window = cmds.window(window_name)
    cmds.showWindow(window)
#-------------------------------------------------------------------
def gui_layout():
    cmds.columnLayout(adjustableColumn=True)
    cmds.rowColumnLayout()
    cmds.columnLayout()
    cmds.button(l='Default_CTRL', c = 'defControl()', h=50, w=300)
    cmds.button(l='ParentShape', c = "cmds.parent(r=1, s=1)", h=50, w=300)
    cmds.button(l='DelConst', c='deleteConst()', h=50, w=300)
    cmds.rowColumnLayout()
    cmds.columnLayout()
    cmds.frameLayout("Recall_Custom_CTRL")
    cmds.textField("name", insertText="")
    cmds.frameLayout("Choose Constraint For FK_Chain")
    cmds.radioCollection("Constraint_Type")
    cmds.radioButton("Parent")
    cmds.radioButton("Orient")
    cmds.button(l='Auto_FK', c='auto_fk()', h=100, w=300)
    cmds.button(l='Auto_IK', c='auto_ik()', h=100, w=300)
    cmds.button(l='Match/Align', c='matcher()', h=100, w=300)
    cmds.button(l='Make_REF', c='make_ref()', h=50, w=300)
    cmds.rowColumnLayout()
    cmds.columnLayout()
    # cmds.button(l='Parent/MO=1', c= 'cmds.parentConstraint(mo=1)', h=50, w=300)
    # cmds.button(l='Orient/MO=1', c = "cmds.orientConstraint(mo=1)", h=50, w=300)
    # cmds.button(l='Point/MO=1', c = "cmds.pointConstraint(mo=1)", h=50, w=300)
#-------------------------------------------------------------------

Rig_Quick_Menue()
gui_layout()

#------------------------------------------------------------------
