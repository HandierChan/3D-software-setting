import os,nuke

# this Folder Path
CurrentFolder = os.path.dirname(__file__)
IconsFolder = '%s/icons' % CurrentFolder
PresetsFolder = '%s/Presets' % CurrentFolder


# Build TTH Toolbar
tthunderToolbar = nuke.toolbar('Nodes').addMenu('TTH', icon='%s/Pipilu.png' % IconsFolder)


# Reveal In Explorer
def RevealInExplorer():
    node = nuke.selectedNode()
    if node.knob("file") is not None:
    #if node.Class()=="Read" or node.Class()=="Write":
        fullpath = node['file'].value()
        os.startfile(os.path.normpath(os.path.dirname(fullpath)))
        # cmd = 'explorer "%s"' % path
        # os.system(cmd)
tthunderToolbar.addCommand('Reveal In Explorer', RevealInExplorer, icon='%s/FileExplorer.png' % IconsFolder)
tthunderToolbar.addSeparator()


# Add Presets
files = os.listdir(PresetsFolder)
files.sort()
for i in files:
    PresetsFullPath = PresetsFolder + '/' + i 
    if os.path.isfile(PresetsFullPath):
        FileName = os.path.splitext(i)[0]
        tthunderToolbar.addCommand(FileName, 'nuke.nodePaste(\"' + PresetsFullPath + '\")', icon='%s/%s.png'%(IconsFolder,FileName))