import os


def getPresetpaths():
    """Return paths for local preset folders"""
    script_file = os.path.realpath(__file__)
    directory = os.path.dirname(script_file)
    localDir = os.path.join(directory, "presets")

    return localDir
