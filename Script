import maya.cmds as cmds

#-------------------------------------------------------------------
def auto_fk(*args):
    ctrl = cmds.textField("name", query=True, text=True)
    has_parent = None
    selection = cmds.ls(sl=True)
    radio = cmds.radioCollection("Constraint_Type", query=True, select=True)
    mode = cmds.radioButton(radio, query=True, label=True)
    
    for i in selection:
        # law el ctrl none aw name bta3oh m4 mawgod fel scene
        if ctrl == None or cmds.objExists(ctrl)==False:
            ctrl = cmds.circle(name = "{}_CTRL".format(i), normal=(0,1,0), radius=2)[0]
        else:
            # e3mel mnnoh duplicate w sammeha
            ctrl = cmds.duplicate(ctrl, name="{}_CTRL".format(i))[0]
        grp = cmds.group(ctrl, name="{}_GRP".format(i))
        pc = cmds.parentConstraint(i,grp, mo=0)
        cmds.delete(pc)
        if i is not None:
            if mode == "Parent":
                cmds.parentConstraint(ctrl, i, mo=1, name="{}_parentConst".format(i))
            elif mode == "Orient":
                cmds.orientConstraint(ctrl,i, mo=1, name="{}_orientConst".format(i))
        if has_parent is not None:
            cmds.parent(grp, has_parent)
        has_parent = ctrl
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
    ctrl = cmds.circle(name = "_CTRL",nrx=1, nry=0, nrz=0, r=2)
    cmds.group(ctrl, name = "_CTRL_GRP")
    cmds.DeleteHistory(ctrl)

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
    cmds.button(l='Match/Align', c='matcher()', h=100, w=300)
    cmds.button(l='Make_REF', c='make_ref()', h=50, w=300)
    cmds.rowColumnLayout()
    cmds.columnLayout()
    cmds.button(l='Parent/MO=1', c= 'cmds.parentConstraint(mo=1)', h=50, w=300)
    cmds.button(l='Orient/MO=1', c = "cmds.orientConstraint(mo=1)", h=50, w=300)
    cmds.button(l='Point/MO=1', c = "cmds.pointConstraint(mo=1)", h=50, w=300)
#-------------------------------------------------------------------

Rig_Quick_Menue()
gui_layout()
