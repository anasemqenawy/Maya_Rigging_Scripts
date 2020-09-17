import maya.cmds as cmds
#-------------------------------------------------------------------
def Transfer_Skin_Weight_Fun():
    sel_list = cmds.ls(sl=True)
    old_geo = sel_list[0]
    new_geo = sel_list[1]
    
    # Get all object history and put it in a list "obj_hist_list"
    obj_hist_listA = cmds.listHistory(old_geo, pdo=True)
    # get the skinclusters from the history list and put them into new list "skin_cluster_list"
    skin_cluster_listA = cmds.ls(obj_hist_listA, type="skinCluster") or None # None here to guarantee to get list
    skin_clusterA = skin_cluster_listA[0]
    # again
    obj_hist_listB = cmds.listHistory(new_geo, pdo=True)
    skin_cluster_listB = cmds.ls(obj_hist_listB, type="skinCluster") or None
    if skin_cluster_listB is None:
        skin_clusterB = None
    else:
        skin_clusterB = skin_cluster_listB[0]
        if skin_clusterB is not None or cmds.objExists(skin_clusterB)==False:
            cmds.delete(skin_clusterB)
    # to get the list of binded joints you MUST put name of the cluster befor query and influence
    binded_jnts_list = cmds.skinCluster(skin_clusterA,query=True,inf=True)
    # bind skin you MUST put the joints "binded_jnts_list" then the geo "new_geo" then the condition >> tsb=True
    cmds.skinCluster(binded_jnts_list,new_geo, tsb=True, name="{}_skin_cluster".format(new_geo))
#-------------------------------------------------------------------
def copy_skin_weight_fun():
    sel_list = cmds.ls(sl=True)
    old_geo = sel_list[0]
    new_geo = sel_list[1]
    # copy weight command
    cmds.CopySkinWeights(noMirror=True, surfaceAssociation = "closestPoint", influenceAssociation = "oneToOne")
#-------------------------------------------------------------------
def Quick_Transfer_Copy_Weight():
    window_name = "Transfer&Copy_Skin_Weight"
    cmds.window(title = window_name,iconName="winTest", height = 50,width = 300)
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    window = cmds.window(window_name)
    cmds.showWindow(window)
#-------------------------------------------------------------------
def gui_layout():
    cmds.columnLayout(adjustableColumn=True)
    cmds.rowColumnLayout()
    cmds.columnLayout()
    cmds.button(l='Transfer_Skin_Weight', c = 'Transfer_Skin_Weight_Fun()', h=100, w=300)
    cmds.rowColumnLayout()
    cmds.columnLayout()
    cmds.button(l='Copy_Skin_Weight', c = 'copy_skin_weight_fun()', h=100, w=300)
#-------------------------------------------------------------------
Quick_Transfer_Copy_Weight()
gui_layout()
#-------------------------------------------------------------------
