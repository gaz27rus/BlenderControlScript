import math
import bpy
import serial;

ob = bpy.data.objects['Armature']

pbone = ob.pose.bones['finger_index.01.R']
pbone.rotation_mode = 'XYZ'
pbone1 = ob.pose.bones['finger_index.02.R']
pbone1.rotation_mode = 'XYZ'
pbone2 = ob.pose.bones['finger_index.03.R']
pbone2.rotation_mode = 'XYZ'

axis = 'X'
angle = 10
ser = serial.Serial('COM3', 9600)
b = []
out = str(ser.readline())
out = out.replace('\\x00', '')
out = out.replace('\\n', '')
out = out.replace('b\'', '')
out = out.replace('\\r', '')
out = out.replace('\'', '')
a = out.split()
for i in a:
        b.append(int(int(i) / 12))
f10 = b[2]
f20 = b[0]
f30 = b[1]
b.clear()

class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"

    limits = bpy.props.IntProperty(default=0)
    _timer = None

    def modal(self, context, event):
        global f10
        global f20
        global f30
        
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
                b.append(int(int(i) / 12))
            f1 = b[2]
            f2 = b[0]
            f3 = b[1]
            if ((f10-f1) != 0):
                pbone.rotation_euler.rotate_axis(axis, math.radians(f1-f10))
                bpy.ops.object.mode_set(mode='OBJECT')
                pbone.keyframe_insert(data_path="rotation_euler" ,frame=1)
                f10 = f1
                
            if ((f20-f2) != 0):
                pbone1.rotation_euler.rotate_axis(axis, math.radians(f2-f20))
                bpy.ops.object.mode_set(mode='OBJECT')
                pbone1.keyframe_insert(data_path="rotation_euler" ,frame=1)
                f20 = f2
                
            if ((f30-f3) != 0):
                pbone2.rotation_euler.rotate_axis(axis, math.radians(f30-f3))
                bpy.ops.object.mode_set(mode='OBJECT')
                pbone2.keyframe_insert(data_path="rotation_euler" ,frame=1)
                f30 = f3
                    
            self.limits += 1
            
            b.clear()
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