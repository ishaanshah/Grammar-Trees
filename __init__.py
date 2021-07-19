import sys
import os
import pathlib

# Check if this add-on is being reloaded
if "bpy" in locals():
    # Reloading .py files
    import importlib

    from . import operator
    from . import menu

    importlib.reload(operator)
    importlib.reload(menu)
# Or if this is the first load of this add-on
else:
    import bpy
    from . import menu

bl_info = {
    "name": "Grammar Trees",
    "author": "Aryamaan Jain, Ishaan Shah",
    "version": 0.1,
    "blender": (2, 90, 0),
    "location": "View 3D > Add > Tree",
    "description": "Adds a tree based on grammar",
    "category": "Development",
}

classes = [*operator.classes, *menu.classes]


def menu_draw(self, context):
    self.layout.operator("curve.gtree_add", text="Add Tree", icon="PLUGIN")


def register():
    for _class in classes:
        bpy.utils.register_class(_class)

    bpy.types.VIEW3D_MT_curve_add.append(menu_draw)


def unregister():
    for _class in classes:
        bpy.utils.unregister_class(_class)

    bpy.types.VIEW3D_MT_curve_add.remove(menu_draw)


if __name__ == "__main__":
    register()
