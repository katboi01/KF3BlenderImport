import bpy
import os
import math

#change this
chara_name = "ch_0088_a"
files_path = "R:\\Assets\\com.sega.KemonoFriends3\\Charas"
#change this

def apply_materials(ob):
    def get_meshes(ob, list, levels=10):
        def recurse(ob, parent, depth, list):
            if depth > levels: 
                return
            if ob.type == 'MESH':
                list.append(ob)
            for child in ob.children:
                recurse(child, ob,  depth + 1, list)
                
        recurse(ob, ob.parent, 0, list)
    print(ob.name)
    mesh_list = []
    get_meshes(main_body, mesh_list)
    for mesh in mesh_list:
        for material in mesh.data.materials:
            print(material.name)
            bsdf = material.node_tree.nodes["Principled BSDF"]
            if len(bsdf.inputs['Base Color'].links):            #skip if texture is already assigned
                continue
            texImage = material.node_tree.nodes.new('ShaderNodeTexImage')
            
            if "body" in material.name:
                texImage.image = bpy.data.images.load(tex_body)
            elif "hair" in material.name:
                texImage.image = bpy.data.images.load(tex_head)
            elif "eye" in material.name:
                texImage.image = bpy.data.images.load(tex_head)
                texImage.image.alpha_mode = 'NONE'
            elif "face" in material.name:
                texImage.image = bpy.data.images.load(tex_face)
            elif "cheek" in material.name:
                texImage.image = bpy.data.images.load(tex_cheek)
                material.blend_method = 'BLEND'
                material.node_tree.links.new(bsdf.inputs['Alpha'], texImage.outputs['Alpha'])
            elif tex_ears != "":
                print("1")
                texImage.image = bpy.data.images.load(tex_ears)
            
            material.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

def get_child(ob, search_for):
    if ob.name.startswith(search_for):
        return ob
    if(len(ob.children) == 0):
        return None
    for child in ob.children:
        return get_child(child, search_for)
                 
def select_object(ob, mode = "EDIT"):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode=mode)
    

chara_id = chara_name.split("_")[1]
chara_costume = chara_name.split("_")[2]

#file paths
body_path = f"{files_path}\\ch_{chara_id}_{chara_costume}\\"

tail_path = f"{files_path}\\ch_{chara_id}_{chara_costume}_tail\\"
if not os.path.exists(tail_path):
    tail_path = f"{files_path}\\ch_{chara_id}_a_tail\\"
    if not os.path.exists(tail_path):
        tail_path = ""

tail_alt_path = f"{files_path}\\ch_{chara_id}_z_tail\\"
if not os.path.exists(tail_alt_path):
    tail_alt_path = ""
        
ears_path = f"{files_path}\\ch_{chara_id}_{chara_costume}_ear\\"
if not os.path.exists(ears_path):
    ears_path = f"{files_path}\\ch_{chara_id}_a_ear\\"
    if not os.path.exists(ears_path):
        ears_path = ""

ears_alt_path = f"{files_path}\\ch_{chara_id}_z_ear\\"
if not os.path.exists(ears_alt_path):
    ears_alt_path = ""
       
print(body_path, tail_path, tail_alt_path, ears_path, ears_alt_path)
 
#textures
tex_body = next((path for path in os.listdir(body_path) if path.endswith("_body.png")), "")
if tex_body != "":
    tex_body = body_path + tex_body
    
tex_face = next((path for path in os.listdir(body_path) if path.endswith("_face.png")), "")
if tex_face != "":
    tex_face = body_path + tex_face
    
tex_head = next((path for path in os.listdir(body_path) if path.endswith("_head.png")), "")
if tex_head != "":
    tex_head = body_path + tex_head

tex_cheek = next((path for path in os.listdir(body_path) if path.endswith(".png") and path.startswith("cheek")), "")
if tex_cheek != "":
    tex_cheek = body_path + tex_cheek

tex_ears = ""
for path in [body_path, ears_path, ears_alt_path, tail_path, tail_alt_path]:
    if path == "": continue
    for file in os.listdir(path):
        if file.lower().endswith("_ear_tail.png"):
            tex_ears = path + file
            break
    if tex_ears != "": break
    
#print(tex_bdy, tex_face, tex_head, tex_cheek, tex_ears)
backslash = "\\"
body_fbx = f"{body_path}{chara_name}.fbx"
ears_fbx = f"{ears_path}{ears_path.split(backslash)[-2]}.fbx" if ears_path != "" else ""
tail_fbx = f"{tail_path}{tail_path.split(backslash)[-2]}.fbx" if tail_path != "" else ""

bpy.ops.object.select_all(action='DESELECT')
body_name = body_path.split(backslash)[-2]
try:
    bpy.ops.import_scene.fbx( filepath = body_fbx )
except:
    pass
main_body = bpy.data.objects[body_name]
main_body.scale = [1,1,1]
main_body.select_set(True)
bpy.ops.object.transform_apply()

objects_to_fix = ["md_eye_base", "md_eye_special_a", "md_eye_special_b", "md_cheek", "md_brow_base"]
for obj in objects_to_fix:
    eyes = bpy.data.objects[obj]
    verts = [i.index for i in eyes.data.vertices]
    group = eyes.vertex_groups.new(name="j_head")
    group.add(verts, 1, "ADD")

try:
    root_armature = bpy.data.objects["root"]
except:
    root_armature = bpy.data.objects[chara_name]
    
for child in root_armature.children:
    if child.name.lower().startswith("md_eye_special"):
        child.hide_set(True)

if ears_fbx != "":
    fail = False
    ears_name = ears_path.split(backslash)[-2]
    bpy.ops.import_scene.fbx( filepath = ears_fbx )
    ears = bpy.data.objects[ears_name]
    ears.scale = [1,1,1]
    ears.location = root_armature.data.bones["j_head"].head_local
    ears.rotation_euler[1] -= math.radians(90)
    
    model = get_child(ears, "model")
    model.name = "md_ears"
    try:	
        model.modifiers[ears.name].object = root_armature	
    except:	
        bpy.ops.object.delete()	
        fail = True
    
    if not fail:
        select_object(model, "OBJECT")
        matrixcopy = model.matrix_world.copy()
        model.parent = root_armature
        model.matrix_world = matrixcopy
            
        select_object(ears)
        ears.data.edit_bones.remove(ears.data.edit_bones["root"])
        
        obs = [root_armature, ears]
        c = {}
        c["object"] = root_armature
        c["active_object"] = root_armature
        c["selected_objects"] = obs
        c["selected_editable_objects"] = obs
        bpy.ops.object.join(c)
        
        select_object(root_armature)
        root_armature.data.edit_bones["j_ear_root"].parent = root_armature.data.edit_bones["j_head"]

if tail_fbx != "":
    fail = False
    tail_name = tail_path.split(backslash)[-2]
    bpy.ops.import_scene.fbx( filepath = tail_fbx )
    tail = bpy.data.objects[tail_name]
    tail.scale = [1,1,1]
    tail.location = root_armature.data.bones["j_lowerbody"].head_local
    
    model = get_child(tail, "model")
    model.name = "md_tail"
    try:	
        model.modifiers[tail.name].object = root_armature	
    except:	
        bpy.ops.object.delete()	
        fail = True
    
    if not fail:
        select_object(model, "OBJECT")
        matrixcopy = model.matrix_world.copy()
        model.parent = root_armature
        model.matrix_world = matrixcopy
            
        select_object(tail)
        tail.data.edit_bones.remove(tail.data.edit_bones["root"])
        
        obs = [root_armature, tail]
        c = {}
        c["object"] = root_armature
        c["active_object"] = root_armature
        c["selected_objects"] = obs
        c["selected_editable_objects"] = obs
        bpy.ops.object.join(c)
        
        select_object(root_armature)
        root_armature.data.edit_bones["j_tail_root"].parent = root_armature.data.edit_bones["j_lowerbody"]

apply_materials(root_armature)
bpy.ops.object.mode_set(mode="OBJECT")