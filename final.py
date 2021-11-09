import math
import bpy
import serial

ob = bpy.data.objects['Armature']

thumb_1 = ob.pose.bones['thumb.01.R']
thumb_1.rotation_mode = 'XYZ'
thumb_2 = ob.pose.bones['thumb.02.R']
thumb_2.rotation_mode = 'XYZ'
thumb_3 = ob.pose.bones['thumb.03.R']
thumb_3.rotation_mode = 'XYZ'

index_0 = ob.pose.bones['palm.01.R']
index_0.rotation_mode = 'XYZ'
index_1 = ob.pose.bones['finger_index.01.R']
index_1.rotation_mode = 'XYZ'
index_2 = ob.pose.bones['finger_index.02.R']
index_2.rotation_mode = 'XYZ'
index_3 = ob.pose.bones['finger_index.03.R']
index_3.rotation_mode = 'XYZ'

middle_0 = ob.pose.bones['palm.02.R']
middle_0.rotation_mode = 'XYZ'
middle_1 = ob.pose.bones['finger_middle.01.R']
middle_1.rotation_mode = 'XYZ'
middle_2 = ob.pose.bones['finger_middle.02.R']
middle_2.rotation_mode = 'XYZ'
middle_3 = ob.pose.bones['finger_middle.03.R']
middle_3.rotation_mode = 'XYZ'

ring_0 = ob.pose.bones['palm.03.R']
ring_0.rotation_mode = 'XYZ'
ring_1 = ob.pose.bones['finger_ring.01.R']
ring_1.rotation_mode = 'XYZ'
ring_2 = ob.pose.bones['finger_ring.02.R']
ring_2.rotation_mode = 'XYZ'
ring_3 = ob.pose.bones['finger_ring.03.R']
ring_3.rotation_mode = 'XYZ'

pinky_0 = ob.pose.bones['palm.04.R']
pinky_0.rotation_mode = 'XYZ'
pinky_1 = ob.pose.bones['finger_pinky.01.R']
pinky_1.rotation_mode = 'XYZ'
pinky_2 = ob.pose.bones['finger_pinky.02.R']
pinky_2.rotation_mode = 'XYZ'
pinky_3 = ob.pose.bones['finger_pinky.03.R']
pinky_3.rotation_mode = 'XYZ'

bones = [middle_1, middle_0, middle_2, thumb_3, thumb_1, thumb_2, ring_3, ring_1, ring_0, ring_2, pinky_3, pinky_2, pinky_0, pinky_1, index_3, index_1, index_2]

axis = 'X'
ser = serial.Serial('COM3', 9600)
angle_previous = []
angle_next = []
out = str(ser.readline())
out = out.replace('\\x00', '')
out = out.replace('\\n', '')
out = out.replace('b\'', '')
out = out.replace('\\r', '')
out = out.replace('\'', '')
a = out.split()
for i in a:
        angle_previous.append(int(int(i) / 75))

class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"

    limits = bpy.props.IntProperty(default=0)
    _timer = None

    def modal(self, context, event):        
        global angle_previous
        global angle_next
        num = 0
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.limits = 0
            self.cancel(context)
            return {'FINISHED'}

        if event.type == 'TIMER':
            
            out = str(ser.readline())
            out = out.replace('\\x00', '')
            out = out.replace('\\n', '')
            out = out.replace('b\'', '')
            out = out.replace('\\r', '')
            out = out.replace('\'', '')
            a = out.split()
            for i in a:
                angle_next.append(int(int(i) / 75))
                
            for i in bones:
                
                rotation_angle = angle_next[num] - angle_previous[num]
                
                if (num == 3 or num == 5 or num == 14 or num == 9 or num == 11 or num == 13 or num == 0):
                    rotation_angle = -(angle_next[num] - angle_previous[num])
                    
                if (num == 1 or num == 4 or num == 8 or num == 12):
                    axis = 'Z'
                else:
                    axis = 'X'
                    
                if (rotation_angle != 0):
                    i.rotation_euler.rotate_axis(axis, math.radians(2*rotation_angle))
                    bpy.ops.object.mode_set(mode='OBJECT')
                    i.keyframe_insert(data_path="rotation_euler" ,frame=1)
                    angle_previous[num] = angle_next[num]
                    
                num += 1   
        angle_next.clear()        
        num = 0                        
        

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(time_step=0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)


def register():
    bpy.utils.register_class(ModalTimerOperator)


def unregister():
    bpy.utils.unregister_class(ModalTimerOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.wm.modal_timer_operator()