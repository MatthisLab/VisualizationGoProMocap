import numpy as np, bpy
from mathutils import Matrix, Vector, Euler

# the array is saved in the file 
arr = np.load(r"/Users/jackieallex/Downloads/markerless-reconstructed/output_3d_skeleton_with_hands.npy") 

#3D array holding [[[x, y, z], [x, y, z]], [[x, y, z], [x, y, z]]] 
#an array of frames, where each frame is an array of points and each point is an array of floats (x, y, z)
  
#the first frame
markers_list = arr[0]

#names of markers 
name_arr = ["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder",
"LElbow", "LWrist", "MidHip", "RHip", "RKnee", "RAnkle", "LHip", "LKnee",
"LAnkle", "REye", "LEye", "REar", "LEar", "LBigToe", "LSmallToe", "LHeel",
"RBigToe", "RSmallToe", "RHeel"]

#use to create bones based on:
order_of_markers = []

#Create empties at marker positions    
name = 0
# make sure project unit is correct for imported data
#Unsure of units
bpy.context.scene.unit_settings.length_unit = 'METERS'
#iterate through arr and create an empty object at that location for each element
for col in markers_list:
    # parse string float value into floats, create Vector, set empty position to Vector
    coord = Vector((float(col[0]), float(col[1]), float(col[2])))
    bpy.ops.object.add(type='EMPTY', location=coord)  
    mt = bpy.context.active_object  
    if (name < 25):
        #get name from name array "name_arr"
        mt.name = name_arr[name]
    elif(name < 46):
        mt.name = "HandR"
    else:
        mt.name = "HandL"
    #add to order_of_markers to facilitate creating bones
    order_of_markers.append(mt)
    #increment index of name of empty in list
    name += 1
    #link empty to scene
    bpy.context.scene.collection.objects.link( mt )
    #set empty's location 
    mt.location = coord
    #set the display size of the empty
    mt.empty_display_size = 0.2
    #sanity check
    #print(coord)
    
print(len(order_of_markers))
print(order_of_markers)
    
#-----------------------------------------------------------------------------------
#Create armature of skeleton if it is the 1st frame

#adds child bone given corresponding parent and empty
#bone tail will appear at the location of empty
def add_child_bone(bone_name, empty1, empty2):
    #Create a new bone
    new_bone = armature_data.data.edit_bones.new(bone_name)
    #Set bone's size
    new_bone.head = (0,0,0)
    new_bone.tail = (0,0.5,0)
    #Set bone's location to wheel
    new_bone.matrix = empty2.matrix_world
    #set location of bone head
    new_bone.head =  empty1.location
    #set location of bone tail
    new_bone.tail = empty2.location
    return new_bone

#Create armature object
armature = bpy.data.armatures.new('Armature')
armature_object = bpy.data.objects.new('Armature', armature)
#Link armature object to our scene
bpy.context.collection.objects.link(armature_object)
#Make armature variable
armature_data = bpy.data.objects[armature_object.name]
#Set armature active
bpy.context.view_layer.objects.active = armature_data
#Set armature selected
armature_data.select_set(state=True)
#Set edit mode
bpy.ops.object.mode_set(mode='EDIT', toggle=False)
#Set bones in front and show axis
armature_data.show_in_front = True
#True to show axis orientation of bones and false to hide it
armature_data.data.show_axes = False

#Add root bone
bone0 = armature_data.data.edit_bones.new('bone0')
#Set its orientation and size
bone0.head = (0,0,0)
bone0.tail = (0,0.5,0)
#Set its location 
bone0.tail = order_of_markers[0].location
bone0.head =  order_of_markers[1].location

#get armature object
def get_armature():
    for ob in bpy.data.objects:
        if ob.type == 'ARMATURE':
            armature = ob
            break
    return armature

armature = get_armature()
    
#bone structure by empties
# https://github.com/CMU-Perceptual-Computing-Lab/openpose/raw/master/doc/media/keypoints_pose_25.png
#bone0: head = 0, tail = 1
#bone1: head = 1, tail = 8
#bone2: head = 8, tail = 12
#bone3: head = 12, tail = 13
#bone4: head = 13, tail = 14
#bone5: head = 14, tail = 21
#bone6: head = 14, tail = 19
#bone7: head = 19, tail = 20
#bone8: head = 8, tail = 9
#bone9: head = 9, tail = 10
#bone10: head = 10, tail = 11
#bone11: head = 11, tail = 24
#bone12: head = 11, tail = 22
#bone13: head = 22, tail = 23
#bone14: head = 1, tail = 5
#bone15: head = 5, tail = 6
#bone16: head = 6, tail = 7
#bone17: head = 1, tail = 2
#bone18: head = 2, tail = 3
#bone19: head = 3, tail = 4
#bone20: head = 0, tail = 16
#bone21: head = 16, tail = 18
#bone22: head = 0, tail = 15
#bone23: head = 15, tail = 17

#Add other bones to armature
bone1 = add_child_bone('bone1', order_of_markers[1], order_of_markers[8])
bone2 = add_child_bone('bone2', order_of_markers[8], order_of_markers[12])
bone3 = add_child_bone('bone3', order_of_markers[12], order_of_markers[13])
bone4 = add_child_bone('bone4', order_of_markers[13], order_of_markers[14])
bone5 = add_child_bone('bone5', order_of_markers[14], order_of_markers[21])
bone6 = add_child_bone('bone6', order_of_markers[14], order_of_markers[19])
bone7 = add_child_bone('bone7', order_of_markers[19], order_of_markers[20])
bone8 = add_child_bone('bone8', order_of_markers[8], order_of_markers[9])
bone9 = add_child_bone('bone9', order_of_markers[9], order_of_markers[10])
bone10 = add_child_bone('bone10', order_of_markers[10], order_of_markers[11])
bone11 = add_child_bone('bone11', order_of_markers[11], order_of_markers[24])
bone12 = add_child_bone('bone12', order_of_markers[11], order_of_markers[22])
bone13 = add_child_bone('bone13', order_of_markers[22], order_of_markers[23])
bone14 = add_child_bone('bone14', order_of_markers[1], order_of_markers[5])
bone15 = add_child_bone('bone15', order_of_markers[5], order_of_markers[6])
bone16 = add_child_bone('bone16', order_of_markers[6], order_of_markers[7])
bone17 = add_child_bone('bone17', order_of_markers[1], order_of_markers[2])
bone18 = add_child_bone('bone18', order_of_markers[2], order_of_markers[3])
bone19 = add_child_bone('bone19', order_of_markers[3], order_of_markers[4])
bone20 = add_child_bone('bone20', order_of_markers[0], order_of_markers[16])
bone21 = add_child_bone('bone21', order_of_markers[16], order_of_markers[18])
bone22 = add_child_bone('bone22', order_of_markers[0], order_of_markers[15])
#the rightEar is not aligning with the rest of the data 
#bone23 = add_child_bone('bone23', order_of_markers[15], order_of_markers[17])

#-----------------------------------------------------------------------------------
# Add hands
#bone structure by empties same for handL (left hand) and handR (right hand)_
# https://github.com/CMU-Perceptual-Computing-Lab/openpose/raw/master/doc/media/keypoints_hand.png
#handL0: head = 0, tail = 1
#handL1: head = 1, tail = 2
#handL2: head = 2, tail = 3
#handL3: head = 3, tail = 4
#handL4: head = 0, tail = 5
#handL5: head = 5, tail = 6
#handL6: head = 6, tail = 7
#handL7: head = 7, tail = 8
#handL8: head = 0, tail = 9
#handL9: head = 9, tail = 10
#handL10: head = 10, tail = 11
#handL11: head = 11, tail = 12
#handL12: head = 0, tail = 13
#handL13: head = 13, tail = 14
#handL14 head = 14, tail = 15
#handL15: head = 15, tail = 16
#handL16: head = 0, tail = 17
#handL17: head = 17, tail = 18
#handL18: head = 18, tail = 19
#handL19: head = 19, tail = 20

#based on marker # from order_of_markers array add bones for hands:
#left hand is 46-66 so add 46 to original 
handL0 = add_child_bone('handL0', order_of_markers[0+46], order_of_markers[1+46])
handL1 = add_child_bone('handL1', order_of_markers[1+46], order_of_markers[2+46])
handL2 = add_child_bone('handL2', order_of_markers[2+46], order_of_markers[3+46])
handL3 = add_child_bone('handL3', order_of_markers[3+46], order_of_markers[4+46])
handL4 = add_child_bone('handL4', order_of_markers[0+46], order_of_markers[5+46])
handL5 = add_child_bone('handL5', order_of_markers[5+46], order_of_markers[6+46])
handL6 = add_child_bone('handL6', order_of_markers[6+46], order_of_markers[7+46])
handL7 = add_child_bone('handL7', order_of_markers[7+46], order_of_markers[8+46])
handL8 = add_child_bone('handL8', order_of_markers[0+46], order_of_markers[9+46])
handL9 = add_child_bone('handL9', order_of_markers[9+46], order_of_markers[10+46])
handL10 = add_child_bone('handL10', order_of_markers[10+46], order_of_markers[11+46])
handL11 = add_child_bone('handL11', order_of_markers[11+46], order_of_markers[12+46])
handL12 = add_child_bone('handL12', order_of_markers[0+46], order_of_markers[13+46])
handL13 = add_child_bone('handL13', order_of_markers[13+46], order_of_markers[14+46])
handL14 = add_child_bone('handL14', order_of_markers[14+46], order_of_markers[15+46])
handL15 = add_child_bone('handL15', order_of_markers[15+46], order_of_markers[16+46])
handL16 = add_child_bone('handL16', order_of_markers[0+46], order_of_markers[17+46])
handL17 = add_child_bone('handL17', order_of_markers[17+46], order_of_markers[18+46])
handL18 = add_child_bone('handL18', order_of_markers[18+46], order_of_markers[19+46])
handL19 = add_child_bone('handL19', order_of_markers[19+46], order_of_markers[20+46])

#right hand is #25-45 so add 25 to original
handR0 = add_child_bone('handR0', order_of_markers[0+25], order_of_markers[1+25])
handR1 = add_child_bone('handR1', order_of_markers[1+25], order_of_markers[2+25])
handR2 = add_child_bone('handR2', order_of_markers[2+25], order_of_markers[3+25])
handR3 = add_child_bone('handR3', order_of_markers[3+25], order_of_markers[4+25])
handR4 = add_child_bone('handR4', order_of_markers[0+25], order_of_markers[5+25])
handR5 = add_child_bone('handR5', order_of_markers[5+25], order_of_markers[6+25])
handR6 = add_child_bone('handR6', order_of_markers[6+25], order_of_markers[7+25])
handR7 = add_child_bone('handR7', order_of_markers[7+25], order_of_markers[8+25])
handR8 = add_child_bone('handR8', order_of_markers[0+25], order_of_markers[9+25])
handR9 = add_child_bone('handR9', order_of_markers[9+25], order_of_markers[10+25])
handR10 = add_child_bone('handR10', order_of_markers[10+25], order_of_markers[11+25])
handR11 = add_child_bone('handR11', order_of_markers[11+25], order_of_markers[12+25])
handR12 = add_child_bone('handR12', order_of_markers[0+25], order_of_markers[13+25])
handR13 = add_child_bone('handR13', order_of_markers[13+25], order_of_markers[14+25])
handR14 = add_child_bone('handR14', order_of_markers[14+25], order_of_markers[15+25])
handR15 = add_child_bone('handR15', order_of_markers[15+25], order_of_markers[16+25])
handR16 = add_child_bone('handR16', order_of_markers[0+25], order_of_markers[17+25])
handR17 = add_child_bone('handR17', order_of_markers[17+25], order_of_markers[18+25])
handR18 = add_child_bone('handR18', order_of_markers[18+25], order_of_markers[19+25])
handR19 = add_child_bone('handR19', order_of_markers[19+25], order_of_markers[20+25])

#-----------------------------------------------------------------------------------
#parent heads and tails to empties
#use bone constraints 
def parent_to_empties(bone_name, head, tail):
    #enter pose mode
    bpy.ops.object.posemode_toggle()
    marker = armature.data.bones[bone_name]
    #Set marker selected
    marker.select = True
    #Set marker active
    bpy.context.object.data.bones.active = marker
    bone = bpy.context.object.pose.bones[bone_name]
    #Copy Location Pose constraint: makes the bone's head follow the given empty
    bpy.ops.pose.constraint_add(type='COPY_LOCATION')
    bone.constraints["Copy Location"].target = head
    #Stretch To Pose constraint: makes the bone's tail follow the given empty
    #stretches the bones to reach the tail to that empty so head location is not affected
    bpy.ops.pose.constraint_add(type='STRETCH_TO')
    bone.constraints["Stretch To"].target = tail
    #exit pose mode
    bpy.ops.object.posemode_toggle()
    
#set parents of heads and tails for each bone 
parent_to_empties('bone0', order_of_markers[0], order_of_markers[1])
parent_to_empties('bone1', order_of_markers[1], order_of_markers[8])
parent_to_empties('bone2', order_of_markers[8], order_of_markers[12])
parent_to_empties('bone3', order_of_markers[12], order_of_markers[13])
parent_to_empties('bone4', order_of_markers[13], order_of_markers[14])
parent_to_empties('bone5', order_of_markers[14], order_of_markers[21])
parent_to_empties('bone6', order_of_markers[14], order_of_markers[19])
parent_to_empties('bone7', order_of_markers[19], order_of_markers[20])
parent_to_empties('bone8', order_of_markers[8], order_of_markers[9])
parent_to_empties('bone9', order_of_markers[9], order_of_markers[10])
parent_to_empties('bone10', order_of_markers[10], order_of_markers[11])
parent_to_empties('bone11', order_of_markers[11], order_of_markers[24])
parent_to_empties('bone12', order_of_markers[11], order_of_markers[22])
parent_to_empties('bone13', order_of_markers[22], order_of_markers[23])
parent_to_empties('bone14', order_of_markers[1], order_of_markers[5])
parent_to_empties('bone15', order_of_markers[5], order_of_markers[6])
parent_to_empties('bone16', order_of_markers[6], order_of_markers[7])
parent_to_empties('bone17', order_of_markers[1], order_of_markers[2])
parent_to_empties('bone18', order_of_markers[2], order_of_markers[3])
parent_to_empties('bone19', order_of_markers[3], order_of_markers[4])
parent_to_empties('bone20', order_of_markers[0], order_of_markers[16])
parent_to_empties('bone21', order_of_markers[16], order_of_markers[18])
parent_to_empties('bone22', order_of_markers[0], order_of_markers[15])
#parent_to_empties('bone23', order_of_markers[15], order_of_markers[17])

parent_to_empties('handL0', order_of_markers[0+46], order_of_markers[1+46])
parent_to_empties('handL1', order_of_markers[1+46], order_of_markers[2+46])
parent_to_empties('handL2', order_of_markers[2+46], order_of_markers[3+46])
parent_to_empties('handL3', order_of_markers[3+46], order_of_markers[4+46])
parent_to_empties('handL4', order_of_markers[0+46], order_of_markers[5+46])
parent_to_empties('handL5', order_of_markers[5+46], order_of_markers[6+46])
parent_to_empties('handL6', order_of_markers[6+46], order_of_markers[7+46])
parent_to_empties('handL7', order_of_markers[7+46], order_of_markers[8+46])
parent_to_empties('handL8', order_of_markers[0+46], order_of_markers[9+46])
parent_to_empties('handL9', order_of_markers[9+46], order_of_markers[10+46])
parent_to_empties('handL10', order_of_markers[10+46], order_of_markers[11+46])
parent_to_empties('handL11', order_of_markers[11+46], order_of_markers[12+46])
parent_to_empties('handL12', order_of_markers[0+46], order_of_markers[13+46])
parent_to_empties('handL13', order_of_markers[13+46], order_of_markers[14+46])
parent_to_empties('handL14', order_of_markers[14+46], order_of_markers[15+46])
parent_to_empties('handL15', order_of_markers[15+46], order_of_markers[16+46])
parent_to_empties('handL16', order_of_markers[0+46], order_of_markers[17+46])
parent_to_empties('handL17', order_of_markers[17+46], order_of_markers[18+46])
parent_to_empties('handL18', order_of_markers[18+46], order_of_markers[19+46])
parent_to_empties('handL19', order_of_markers[19+46], order_of_markers[20+46])

parent_to_empties('handR0', order_of_markers[0+25], order_of_markers[1+25])
parent_to_empties('handR1', order_of_markers[1+25], order_of_markers[2+25])
parent_to_empties('handR2', order_of_markers[2+25], order_of_markers[3+25])
parent_to_empties('handR3', order_of_markers[3+25], order_of_markers[4+25])
parent_to_empties('handR4', order_of_markers[0+25], order_of_markers[5+25])
parent_to_empties('handR5', order_of_markers[5+25], order_of_markers[6+25])
parent_to_empties('handR6', order_of_markers[6+25], order_of_markers[7+25])
parent_to_empties('handR7', order_of_markers[7+25], order_of_markers[8+25])
parent_to_empties('handR8', order_of_markers[0+25], order_of_markers[9+25])
parent_to_empties('handR9', order_of_markers[9+25], order_of_markers[10+25])
parent_to_empties('handR10', order_of_markers[10+25], order_of_markers[11+25])
parent_to_empties('handR11', order_of_markers[11+25], order_of_markers[12+25])
parent_to_empties('handR12', order_of_markers[0+25], order_of_markers[13+25])
parent_to_empties('handR13', order_of_markers[13+25], order_of_markers[14+25])
parent_to_empties('handR14', order_of_markers[14+25], order_of_markers[15+25])
parent_to_empties('handR15', order_of_markers[15+25], order_of_markers[16+25])
parent_to_empties('handR16', order_of_markers[0+25], order_of_markers[17+25])
parent_to_empties('handR17', order_of_markers[17+25], order_of_markers[18+25])
parent_to_empties('handR18', order_of_markers[18+25], order_of_markers[19+25])
parent_to_empties('handR19', order_of_markers[19+25], order_of_markers[20+25])


#-----------------------------------------------------------------------------------
# Animate! 
#find number of frames in animation
num_frames = len(arr) #500 frames at 120 fps
    
#create a new handler to change empty positions every frame
def my_handler(scene): 
    frames_seen = 0
    #must be in pose mode to set keyframes
    bpy.ops.object.mode_set(mode='POSE')
    #keep track of current_marker
    current_marker = 0
    #find the current frame number
    frame = scene.frame_current
    #get the list of marker points from the current frame
    markers_list = arr[frame]
    #iterate through list of markers in this frame
    for col in markers_list:
        coord = Vector((float(col[0]), float(col[1]), float(col[2])))
        empty = order_of_markers[current_marker] 
        #change empty position : this is where the change in location every frame happens
        empty.location = coord
        #Set keyframes of the empty location at this frame to save the animation
        #empty.keyframe_insert(data_path='location',frame=scene.frame_current)
        #increment counter of the number marker we are currently changing
        current_marker += 1 
        #future... may want to continue to look into how to keyframe each bone in amrature
        if(current_marker == len(markers_list)):
            frames_seen += 1
            for bone in bpy.data.objects['Armature'].pose.bones:
                bpy.ops.pose.visual_transform_apply()
                bone.keyframe_insert(data_path = 'location')
                if bone.rotation_mode == "QUATERNION":
                    bone.keyframe_insert(data_path = 'rotation_quaternion')
                else:
                    bone.keyframe_insert(data_path = 'rotation_euler')
                #bone.keyframe_insert(data_path = 'scale')
    if (frames_seen == 500):
        unregister();
        
        
                
#-----------------------------------------------------------------------------------
#bake action from keyframes 
#bpy.ops.nla.bake(frame_start=0, frame_end=num_frames, only_selected=True, visual_keying=True, clear_constraints=False, use_current_action=False, bake_types={'POSE'})
            
#print ("Action: {}, First frame: {}, Second frame: {}".format(a.name, firstFrame, lastFrame))


#bpy.ops.nla.bake(frame_start=1, frame_end=250, step=1, only_selected=True, visual_keying=False, clear_constraints=False, clear_parents=False, use_current_action=False, bake_types={'POSE'})
#-----------------------------------------------------------------------------------
#function to register custom handler
def register():
   bpy.app.handlers.frame_change_post.append(my_handler)
   
def unregister():
    bpy.app.handlers.frame_change_post.remove(my_handler)
    
register()