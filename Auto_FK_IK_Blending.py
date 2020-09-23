import maya.cmds as cmds

window_name = "Auto_FK_IK_Blending"
cmds.window(title=window_name, iconName="winTest")

if cmds.window(window_name, exists=True):
    cmds.deleteUI(window_name)
window = cmds.window(window_name)
cmds.showWindow(window)
#-------------------------------------------------------------------
cmds.rowColumnLayout(nc=2)
cmds.button(label="Main_Joint_List", command="main()", w=150, h=50)
cmds.button(label="FK/IK_Blend", command="fk_ik_blend()", w=150, h=50)
cmds.button(label="FK_Joint_List", command="fk()", w=150, h=50)
cmds.button(label="IK_Joint_List", command="ik()", w=150, h=50)
#-------------------------------------------------------------------
fk_list=[]
ik_list=[]
main_list=[]
#-------------------------------------------------------------------
def fk():
    selection = cmds.ls(sl=True)
    for i in selection:
        fk_list.append(i)
    print(fk_list)       
#-------------------------------------------------------------------
def ik():
    selection = cmds.ls(sl=True)
    for i in selection:
        ik_list.append(i)
    print(ik_list)
#-------------------------------------------------------------------
def main():
    selection = cmds.ls(sl=True)
    for i in selection:
        main_list.append(i)
    print(main_list)
#-------------------------------------------------------------------
def fk_ik_blend():
    swtch_ctrl = "Fk_Ik_Switch"
    cmds.circle(name = swtch_ctrl, normal=(0,1,0), radius=3)
    cmds.addAttr(swtch_ctrl, ln="FK_IK", at= "double", min = 0, max= 1, keyable=1,hidden=0, readable=1)
    swtch_ctrl_grp = cmds.group(em=True, name="{}_Grp".format(swtch_ctrl))
    cmds.parent(swtch_ctrl, swtch_ctrl_grp)
    cmds.DeleteHistory(swtch_ctrl)
    pc = cmds.pointConstraint(main_list[2], swtch_ctrl_grp, mo=0)
    cmds.delete(pc)
    #---------------------------------------------------------
    shoulder_blend_node = None
    if shoulder_blend_node == None or cmds.objExists(shoulder_blend_node)==False:
            shoulder_blend_node = "FK_IK_{}_Blend".format(main_list[0])
    else : 
        shoulder_blend_node = shoulder_blend_node
        
    elbow_blend_node = "FK_IK_{}_Blend".format(main_list[1])
    if shoulder_blend_node == None or cmds.objExists(elbow_blend_node)==False:
           elbow_blend_node = "FK_IK_{}_Blend".format(main_list[1])
    else : 
        elbow_blend_node = elbow_blend_node
    wrist_blend_node = "FK_IK_{}_Blend".format(main_list[2])
    if wrist_blend_node == None or cmds.objExists(wrist_blend_node)==False:
            wrist_blend_node = "FK_IK_{}_Blend".format(main_list[2])
    else : 
        wrist_blend_node = wrist_blend_node
    #---------------------------------------------------------
    cmds.shadingNode("blendColors", name=shoulder_blend_node, asUtility=True)
    cmds.connectAttr("{}.rotate".format(fk_list[0]), "{}.color2".format(shoulder_blend_node))
    cmds.connectAttr("{}.rotate".format(ik_list[0]), "{}.color1".format(shoulder_blend_node))
    cmds.connectAttr("{}.FK_IK".format(swtch_ctrl), "{}.blender".format(shoulder_blend_node))
    cmds.connectAttr("{}.output".format(shoulder_blend_node), "{}.rotate".format(main_list[0]))
    #---------------------------------------------------------
    cmds.shadingNode("blendColors", name=elbow_blend_node, asUtility=True)
    cmds.connectAttr("{}.rotate".format(fk_list[1]), "{}.color2".format(elbow_blend_node))
    cmds.connectAttr("{}.rotate".format(ik_list[1]), "{}.color1".format(elbow_blend_node))
    cmds.connectAttr("{}.FK_IK".format(swtch_ctrl), "{}.blender".format(elbow_blend_node))
    cmds.connectAttr("{}.output".format(elbow_blend_node), "{}.rotate".format(main_list[1]))
    #---------------------------------------------------------
    cmds.shadingNode("blendColors", name=wrist_blend_node, asUtility=True)
    cmds.connectAttr("{}.rotate".format(fk_list[2]), "{}.color2".format(wrist_blend_node))
    cmds.connectAttr("{}.rotate".format(ik_list[2]), "{}.color1".format(wrist_blend_node))
    cmds.connectAttr("{}.FK_IK".format(swtch_ctrl), "{}.blender".format(wrist_blend_node))
    cmds.connectAttr("{}.output".format(wrist_blend_node), "{}.rotate".format(main_list[2]))





