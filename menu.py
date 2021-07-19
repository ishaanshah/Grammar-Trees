import os

import bpy

from . import utils


class PresetMenu(bpy.types.Menu):
    """
    Create the preset menu by finding all preset files
    in the preset directory
    """

    bl_idname = "GTREE_MT_preset"  # was sapling.presetmenu
    bl_label = "Presets"

    def draw(self, context):
        # Get all the sapling presets
        presets = [a for a in os.listdir(utils.getPresetpaths()) if a[-5:] == ".json"]
        layout = self.layout
        layout.separator()
        for p in presets:
            layout.operator("gtree.importdata", text=p[:-5]).filename = p
        layout.separator()


classes = [PresetMenu]
