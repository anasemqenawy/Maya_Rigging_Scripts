import sys
import maya.cmds as cmds
#---------------------------------------------------------
def fk_ik_blend(*args):
     #---------------------------------------------------------
    # swtch_ctrl = cmds.textField("name", query=True, text=True)
    swtch_ctrl = None
    swtch_ctrl_grp = None
    #---------------------------------------------------------
    sel = cmds.ls(sl=True)
    jnt_list = []
    fk_list = []
    ik_list = []
    shoulder_blend_node = None
    elbow_blend_node = None
    wrist_blend_node = None
    #---------------------------------------------------------
    for i in sel:
        x = i.lower()
        if "_fk" in x:
            fk_list.append(x)
        elif "_ik" in x:
            ik_list.append(x)
        else:
            jnt_list.append(x)
    #---------------------------------------------------------
    if swtch_ctrl == None or cmds.objExists(swtch_ctrl)==False:
            swtch_ctrl = cmds.circle(name = "Fk_Ik_Switch", normal=(0,1,0), radius=3)[0]
    else:
            swtch_ctrl = cmds.duplicate(swtch_ctrl, name="Fk_Ik_Switch")[0]
    #---------------------------------------------------------
    cmds.addAttr(swtch_ctrl, ln="FK_IK", at= "double", min = 0, max= 1, keyable=1,hidden=0, readable=1)
    if swtch_ctrl_grp == None or cmds.objExists(swtch_ctrl_grp)==False:
        swtch_ctrl_grp = cmds.group(em=True, name = "FK_IK_SWITCH_GRP")
    else:
        cmds.delete(swtch_ctrl_grp)
        swtch_ctrl_grp = cmds.group(em=True, name = "FK_IK_SWITCH_GRP")
    cmds.parent(swtch_ctrl, swtch_ctrl_grp)
    cmds.DeleteHistory(swtch_ctrl)
    #---------------------------------------------------------
    l = len(jnt_list)
    align = cmds.parentConstraint(jnt_list[l-1], swtch_ctrl_grp, mo=0)
    cmds.delete(align)
    #---------------------------------------------------------
    if shoulder_blend_node == None or cmds.objExists(shoulder_blend_node)==False:
        shoulder_blend_node = "FK_IK_{}_Blend".format(jnt_list[0])
    else:
        cmds.delete(shoulder_blend_node)
        shoulder_blend_node = "FK_IK_{}_Blend".format(jnt_list[0])
    if elbow_blend_node == None or cmds.objExists(elbow_blend_node)==False:
        elbow_blend_node = "FK_IK_{}_Blend".format(jnt_list[1])
    else:
        cmds.delete(elbow_blend_node)
        elbow_blend_node = "FK_IK_{}_Blend".format(jnt_list[1])
    if wrist_blend_node == None or cmds.objExists(wrist_blend_node)==False:
        wrist_blend_node = "FK_IK_{}_Blend".format(jnt_list[2])
    else:
        cmds.delete(wrist_blend_node)
        wrist_blend_node = "FK_IK_{}_Blend".format(jnt_list[2])
    #---------------------------------------------------------
    cmds.shadingNode("blendColors", name=shoulder_blend_node, asUtility=True)
    cmds.connectAttr("{}.rotate".format(fk_list[0]), "{}.color2".format(shoulder_blend_node))
    cmds.connectAttr("{}.rotate".format(ik_list[0]), "{}.color1".format(shoulder_blend_node))
    cmds.connectAttr("{}.FK_IK".format(swtch_ctrl), "{}.blender".format(shoulder_blend_node))
    cmds.connectAttr("{}.output".format(shoulder_blend_node), "{}.rotate".format(jnt_list[0]))
    #---------------------------------------------------------
    cmds.shadingNode("blendColors", name=elbow_blend_node.format(jnt_list[1]), asUtility=True)
    cmds.connectAttr("{}.rotate".format(fk_list[1]), "{}.color2".format(elbow_blend_node))
    cmds.connectAttr("{}.rotate".format(ik_list[1]), "{}.color1".format(elbow_blend_node))
    cmds.connectAttr("{}.FK_IK".format(swtch_ctrl), "{}.blender".format(elbow_blend_node))
    cmds.connectAttr("{}.output".format(elbow_blend_node), "{}.rotate".format(jnt_list[1]))
    #---------------------------------------------------------
    cmds.shadingNode("blendColors", name=wrist_blend_node.format(jnt_list[2]), asUtility=True)
    cmds.connectAttr("{}.rotate".format(fk_list[2]), "{}.color2".format(wrist_blend_node))
    cmds.connectAttr("{}.rotate".format(ik_list[2]), "{}.color1".format(wrist_blend_node))
    cmds.connectAttr("{}.FK_IK".format(swtch_ctrl), "{}.blender".format(wrist_blend_node))
    cmds.connectAttr("{}.output".format(wrist_blend_node), "{}.rotate".format(jnt_list[2]))
    #---------------------------------------------------------
fk_ik_blend()
