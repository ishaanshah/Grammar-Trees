import json
import os
import time

import bpy
from bpy.props import BoolProperty, FloatProperty, IntProperty, StringProperty

from . import tree_grammar
from . import menu
from . import utils

props = {}
use_props = True
is_first = True


class ImportData(bpy.types.Operator):
    """This operator handles importing existing presets"""

    bl_idname = "gtree.importdata"
    bl_label = "Import Preset"

    filename: StringProperty()

    def execute(self, context):
        global props, use_props

        # Read the preset data into the global settings
        try:
            f = open(os.path.join(utils.getPresetpaths(), self.filename), "r")
        except (FileNotFoundError, IOError):
            # TODO: Error handling
            pass

        try:
            props = json.load(f)
        except json.JSONDecodeError:
            # TODO: Error handling
            pass

        f.close()

        # Set the flag to use the settings
        use_props = True
        return {"FINISHED"}


class AddTree(bpy.types.Operator):
    bl_idname = "curve.gtree_add"
    bl_label = "Add Tree"
    bl_options = {"REGISTER", "UNDO"}

    def update_tree(self, context):
        self.do_update = True

    def no_update_tree(self, context):
        self.do_update = False

    do_update: BoolProperty(name="Do Update", default=True, options={"HIDDEN"})
    seed: IntProperty(
        name="Random Seed",
        description="The seed of the random number generator",
        default=0,
        update=update_tree,
    )
    levels: IntProperty(
        name="Levels",
        description="Number of recursive branches",
        min=1,
        max=15,
        soft_max=10,
        default=3,
        update=update_tree,
    )
    initial_width: FloatProperty(
        name="Initial Width",
        description="Initial width of the tree",
        min=0.0,
        default=0.1,
        update=update_tree,
    )

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "seed")
        layout.prop(self, "levels")
        layout.prop(self, "initial_width")
        layout.menu("GTREE_MT_preset", text="Load Preset")

    def execute(self, context):
        global props, use_props, is_first

        # Load pine preset on first run
        if is_first:
            bpy.ops.gtree.importdata(filename="pine.json")

        if use_props:
            # Update properties if preset is changed
            self.levels = props["max_recursion_depth"]
            self.initial_width = (
                props["initial_width"][0] + props["initial_width"][1]
            ) / 2
        else:
            # Update props as per change in properties
            props["max_recursion_depth"] = self.levels
            props["initial_width"] = [self.initial_width, self.initial_width]

        tree_grammar.TreeGrammar(props).draw(self.seed)
        is_first = False
        use_props = False

        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


classes = [ImportData, AddTree]
