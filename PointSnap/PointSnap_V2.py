import maya.cmds as cmds  
import random  
import maya.mel as mel  

# 全局变量以存储 UV 和点的位置  
uv_positions = []  
point_positions = []  
recorded_point_color = None  
recorded_uv_color = None  

######################### UV吸附相关 ########################################################  
def record_uv_positions_func(*args):  
    global uv_positions  
    selected_uvs = cmds.ls(sl=True, fl=True)  
    if not selected_uvs:  
        cmds.error("请先选择一些 UV 点！")  
    
    uv_positions = []  
    for uv in selected_uvs:  
        pos = cmds.polyEditUV(uv, q=True)  
        uv_positions.append(pos)  

    global recorded_uv_color  
    recorded_uv_color = random_gray_color()  
    change_button_color('button3', recorded_uv_color)  

def move_uvs_to_positions_func(*args):  
    global uv_positions  
    selected_uvs = cmds.ls(sl=True, fl=True)  
    if len(selected_uvs) != len(uv_positions):  
        cmds.error("新选择的 UV 点数量必须与记录的 UV 点数量相同！")  
    
    for uv, pos in zip(selected_uvs, uv_positions):  
        current_pos = cmds.polyEditUV(uv, q=True)  
        cmds.polyEditUV(uv, u=pos[0] - current_pos[0], v=pos[1] - current_pos[1])  

    if recorded_uv_color is not None:  
        change_button_color('button4', recorded_uv_color)  

##########################################################################################  
def select_and_add_vertices():  
    selected_points = []  
    selected_vertices = cmds.ls(selection=True, flatten=True)  
    print("Selected vertices:", selected_vertices)  

    if not selected_vertices:  
        print("No vertices selected.")  
        return selected_points  

    selected_vertex = cmds.ls(orderedSelection=1)[0]  
    selected_points.append(selected_vertex)  
    print("Added vertex to selected_points:", selected_points)  
    cmds.select(selected_vertex)  

    def add_selected_vertices():  
        nonlocal selected_points  
        mel.eval('PolySelectTraverse 1')  
        poly_select_traverse_vertices = cmds.ls(selection=True, flatten=True)  
        selected_vertices_set = set(selected_vertices)  
        poly_select_traverse_set = set(poly_select_traverse_vertices)  
        selected_points_set = set(selected_points)  
        common_vertices = poly_select_traverse_set.intersection(selected_vertices_set)  
        print("Common vertices:", common_vertices)  
        filtered_vertices = common_vertices - selected_points_set  
        print("Filtered vertices:", filtered_vertices)  
        selected_points.extend(filtered_vertices)  
        print("Updated selected_points:", selected_points)  
        cmds.select(filtered_vertices)  

    for _ in range(len(selected_vertices)):  
        add_selected_vertices()  

    return selected_points  

def record_selected_points(*args):  
    global point_positions  
    point_positions.clear()  # 清空之前记录的点位置  
    selected_points = select_and_add_vertices()  # 获取选择的点  

    for pt in selected_points:  
        pos = cmds.xform(pt, q=True, ws=True, t=True)  
        point_positions.append((pt, pos))  

    global recorded_point_color  
    recorded_point_color = random_gray_color()  
    change_button_color('button1', recorded_point_color)  
    print("记录的点和位置:")  
    for pt, pos in point_positions:  
        print(f"点: {pt}, 位置: {pos}")  

def set_points_to_recorded_positions_func(*args):  
    global point_positions  

    selection = select_and_add_vertices()  
    if not point_positions:  # 如果没有记录的点，提供友好的提示  
        cmds.error("错误: 没有记录的点位置。")  
        return  

    if len(selection) != len(point_positions):  
        cmds.error("错误: 选择的点数量与记录的点数量不匹配。")  
        return  
    
    for i, pt in enumerate(selection):  
        pos = point_positions[i][1]  
        cmds.xform(pt, ws=True, t=pos)  
    
    if recorded_point_color is not None:  
        change_button_color('button2', recorded_point_color)  

##################### 创建窗口 #####################  
def random_gray_color(min_gray=0.4, max_gray=0.6, color_variation=0.2):  
    base_gray = random.uniform(min_gray, max_gray)  
    offset_r = random.uniform(-color_variation, color_variation)  
    offset_g = random.uniform(-color_variation, color_variation)  
    offset_b = random.uniform(-color_variation, color_variation)  
    
    r = max(0, min(1, base_gray + offset_r))  
    g = max(0, min(1, base_gray + offset_g))  
    b = max(0, min(1, base_gray + offset_b))  
    
    return (r, g, b)  # 返回生成的RGB值  

def change_button_color(button_name, color):  
    """更改按钮颜色的函数"""  
    cmds.button(button_name, edit=True, bgc=color)  

def SnapPointTool():  
    if cmds.window("Window", exists=True):  
        cmds.deleteUI("Window", window=True)  
    
    window = cmds.window("Window", title='拓扑修改工具', widthHeight=(220, 100))  
    cmds.columnLayout(adjustableColumn=False)  
    cmds.button('button1', w=220, label='记录 点位置', command=record_selected_points)  
    cmds.button('button2', w=220, label='移动 点位置', command=set_points_to_recorded_positions_func)   
    cmds.button('button3', w=220, label='记录 UV 点', command=record_uv_positions_func)  
    cmds.button('button4', w=220, label='移动 UV 点', command=move_uvs_to_positions_func)  
    cmds.showWindow(window)  

SnapPointTool()