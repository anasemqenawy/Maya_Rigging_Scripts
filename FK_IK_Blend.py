import maya.cmds as cmds

def fk_ik_blend():
    jnt_list = []
    fk_list = []
    ik_list = []
    sel = cmds.ls(sl=True)
    for i in sel:
        x=i
        if "_fk" in x:
            fk_list.append(x)
        if "_ik" in x:
            ik_list.append(x)
        else:
            jnt_list.append(x)
    cmds.parentConstraint(fk_list[0], ik_list[0], jnt_list[0], mo=0)
    cmds.parentConstraint(fk_list[1], ik_list[1], jnt_list[1], mo=0)
    cmds.parentConstraint(fk_list[2], ik_list[2], jnt_list[2], mo=0)

if __init__ == "main":
    fk_ik_blend()