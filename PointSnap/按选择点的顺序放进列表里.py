import maya.cmds as cmds  
import maya.mel as mel  
##使用方：法点选第一个点 然后按住shift双击最后一个点会选中一排的点
##执行脚本 也许 大概其 应该 差不多就会按照点ID排序的方式放进selected_points这个变量里了，不然maya总会进行一个从小到大的排序
##可能哪里会有bug，but我一个建模的就这样吧，感谢群里大佬提供了思路和脚本
def select_and_add_vertices():  
    selected_points = []  
    
    # 获取当前选择的多边形顶点  
    selected_vertices = cmds.ls(selection=True, flatten=True)  
    print("Selected vertices:", selected_vertices)  

    if not selected_vertices:  
        print("No vertices selected.")  
        return selected_points  

    # 选择第一个选择的点并将其添加到selected_points中  
    selected_vertex = cmds.ls(orderedSelection=1)[0]  
    selected_points.append(selected_vertex)  
    print("Added vertex to selected_points:", selected_points)  

    cmds.select(selected_vertex)  

    def add_selected_vertices():  
        nonlocal selected_points  # 访问外部的 selected_points  
        # 扩展选择  
        mel.eval('PolySelectTraverse 1')  
        # 将所有扩展的点加进集合里  
        poly_select_traverse_vertices = cmds.ls(selection=True, flatten=True)  

        # 将一开始选择的那些点加进集合里  
        selected_vertices_set = set(selected_vertices)  
        # 将扩展的点加进集合里  
        poly_select_traverse_set = set(poly_select_traverse_vertices)  
        # 将选择的第一个点加进一个集合里  
        selected_points_set = set(selected_points)  
        # 并集计算得出公共的点  
        common_vertices = poly_select_traverse_set.intersection(selected_vertices_set)  
        print("Common vertices:", common_vertices)  

        filtered_vertices = common_vertices - selected_points_set  
        print("Filtered vertices:", filtered_vertices)  

        selected_points.extend(filtered_vertices)  
        print("Updated selected_points:", selected_points)  

        cmds.select(filtered_vertices)  

    # 添加 for 循环来调用函数，次数为 len(selected_vertices)  
    for _ in range(len(selected_vertices)):  
        add_selected_vertices()  

    return selected_points  # 返回最终的 selected_points  

select_and_add_vertices()

