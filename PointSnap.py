import maya.cmds as cmds  
import random  

# 全局变量以存储 UV 位置  
uv_positions = []  

# 用于存储点的位置  
point_positions = []  
# 记录按钮颜色的变量  
recorded_point_color = None  
recorded_uv_color = None  

def random_gray_color(min_gray=0.4, max_gray=0.6, color_variation=0.2):  
    """生成带有随机颜色倾向的高级灰色，即使其不完美灰色"""  
    base_gray = random.uniform(min_gray, max_gray)  # 生成基础灰色值  
    # 随机生成偏移量，确保加入的偏差不会使颜色过于饱和  
    offset_r = random.uniform(-color_variation, color_variation)  
    offset_g = random.uniform(-color_variation, color_variation)  
    offset_b = random.uniform(-color_variation, color_variation)  
    
    # 确保生成的颜色值在0到1之间  
    r = max(0, min(1, base_gray + offset_r))  
    g = max(0, min(1, base_gray + offset_g))  
    b = max(0, min(1, base_gray + offset_b))  
    
    return (r, g, b)  # 返回生成的RGB值  

def change_button_color(button_name, color):  
    """更改按钮颜色的函数"""  
    cmds.button(button_name, edit=True, bgc=color)  

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

def record_selected_points(*args):  
    global point_positions  
    selection = cmds.ls(selection=True, fl=True)  
    if not selection:  
        cmds.error("请先选择一些点！")  
    
    point_positions = []  
    for pt in selection:  
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
    selection = cmds.ls(selection=True, fl=True)  
    if len(selection) != len(point_positions):  
        cmds.error("错误: 选择的点数量与记录的点数量不匹配。")  
        return  
    
    for i, pt in enumerate(selection):  
        pos = point_positions[i][1]  
        cmds.xform(pt, ws=True, t=pos)  
    
    if recorded_point_color is not None:  
        change_button_color('button2', recorded_point_color)  

def create_uv_window():  
    if cmds.window('uvWindow', exists=True):  
        cmds.deleteUI('uvWindow')  

    cmds.window('uvWindow', title='UV 点工具', widthHeight=(200, 100))  
    cmds.columnLayout(adjustableColumn=True)  

    cmds.button('button1', label='记录 点位置', command=record_selected_points)  
    cmds.button('button2', label='移动 点位置', command=set_points_to_recorded_positions_func)   
    cmds.button('button3', label='记录 UV 点', command=record_uv_positions_func)  
    cmds.button('button4', label='移动 UV 点', command=move_uvs_to_positions_func)  

    cmds.setParent('..')  
    cmds.showWindow('uvWindow')  

# 调用函数创建窗口  
create_uv_window()