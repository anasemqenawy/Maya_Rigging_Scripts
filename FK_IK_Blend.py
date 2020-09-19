import sys
import maya.cmds as cmds
#---------------------------------------------------------
def fk_ik_blend(*args):
    #---------------------------------------------------------
    swtch_ctrl = cmds.textField("name", query=True, text=True)
    if swtch_ctrl == None or cmds.objExists(swtch_ctrl)==False:
            swtch_ctrl = cmds.circle(name = "Fk_Ik_Switch", normal=(0,1,0), radius=3)[0]
    else:
            swtch_ctrl = cmds.duplicate(swtch_ctrl, name="Fk_Ik_Switch")[0]
    cmds.addAttr(swtch_ctrl, ln="FK_IK", at= "double", min = 0, max= 1, keyable=1,hidden=0, readable=1)
    grp = cmds.group(em=True, name="{}_Grp".format(swtch_ctrl))
    cmds.parent(swtch_ctrl, grp)
    cmds.DeleteHistory(swtch_ctrl)
    #---------------------------------------------------------
    jnt_list = []
    fk_list = []
    ik_list = []
    sel = cmds.ls(sl=True)
    #---------------------------------------------------------
    for i in sel:
        x=i.lower()
        if "_fk" in x:
            fk_list.append(x)
        if "_ik" in x:
            ik_list.append(x)
        else:
            jnt_list.append(x)
    #---------------------------------------------------------
    l = len(jnt_list)
    pc = cmds.pointConstraint(jnt_list[l-1], grp, mo=0)
    cmds.delete(pc)
    #---------------------------------------------------------
    shouldr_constraint = jnt_list[0]+"_constraint"
    shouldr_list = shouldr_constraint.split("_")
    elbow_constraint = jnt_list[1]+"_constraint"
    elbow_list = elbow_constraint.split("_")
    wrst_constraint = jnt_list[2]+"_constraint"
    wrst_list = wrst_constraint.split("_")
    cmds.parentConstraint(fk_list[0], ik_list[0], jnt_list[0], mo=0, name="{}".format(shouldr_constraint))
    cmds.parentConstraint(fk_list[1], ik_list[1], jnt_list[1], mo=0, name="{}".format(elbow_constraint))
    cmds.parentConstraint(fk_list[2], ik_list[2], jnt_list[2], mo=0, name="{}".format(wrst_constraint))
    
    #---------------------------------------------------------
    rev_node = "fk_ik_reverse"
    if rev_node == None or cmds.objExists(rev_node)==False:
        cmds.shadingNode("reverse", name = "{}".format(rev_node), asUtility=True)
    else:
        rev_node = rev_node
    cmds.connectAttr("Fk_Ik_Switch.FK_IK", "{}.{}_{}_ikW1".format(shouldr_constraint, shouldr_list[0], shouldr_list[1]))
    cmds.connectAttr("Fk_Ik_Switch.FK_IK", "{}.{}_{}_ikW1".format(elbow_constraint, elbow_list[0], elbow_list[1]))
    cmds.connectAttr("Fk_Ik_Switch.FK_IK", "{}.{}_{}_ikW1".format(wrst_constraint, wrst_list[0], wrst_list[1]))
    cmds.connectAttr("Fk_Ik_Switch.FK_IK", "fk_ik_reverse.inputX")
    #---------------------------------------------------------
    cmds.connectAttr("fk_ik_reverse.outputX", "{}.{}_{}_fkW0".format(shouldr_constraint, shouldr_list[0], shouldr_list[1]))
    cmds.connectAttr("fk_ik_reverse.outputX", "{}.{}_{}_fkW0".format(elbow_constraint, elbow_list[0], elbow_list[1]))
    cmds.connectAttr("fk_ik_reverse.outputX", "{}.{}_{}_fkW0".format(wrst_constraint, wrst_list[0], wrst_list[1]))
    #---------------------------------------------------------
fk_ik_blend() 
