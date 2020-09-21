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
    swtch_ctrl_grp = cmds.group(em=True, name="{}_Grp".format(swtch_ctrl))
    cmds.parent(swtch_ctrl, swtch_ctrl_grp)
    cmds.DeleteHistory(swtch_ctrl)
    #---------------------------------------------------------
    sel = cmds.ls(sl=True)
    jnt_list = []
    fk_list = []
    ik_list = []
    for i in sel:
        x = i.lower()
        if "_fk" in x:
            fk_list.append(x)
        elif "_ik" in x:
            ik_list.append(x)
        else:
            jnt_list.append(x)
    #---------------------------------------------------------
    pc = cmds.pointConstraint(jnt_list[2], swtch_ctrl_grp, mo=0)
    cmds.delete(pc)
    #---------------------------------------------------------
    shoulder_blend_node = "FK_IK_{}_Blend".format(jnt_list[0])
    elbow_blend_node = "FK_IK_{}_Blend".format(jnt_list[1])
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

fk_ik_blend(*args)
