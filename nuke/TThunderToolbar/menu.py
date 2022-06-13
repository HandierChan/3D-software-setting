import os,nuke

# this Folder Path
tthToolbarCurrentFolder = os.path.dirname(__file__)
tthToolbarIconsFolder = '%s/icons' % tthToolbarCurrentFolder
tthToolbarPresetsFolder = '%s/Presets' % tthToolbarCurrentFolder


# Build TTH Toolbar
tthunderToolbar = nuke.toolbar('Nodes').addMenu('TTH', icon='%s/Pipilu.png' % tthToolbarIconsFolder)


# Open File Directory
def openFileDirectory():
    #if node.Class()=="Read" or node.Class()=="Write":
    if nuke.selectedNodes():
        nodeFilePath=nuke.filename(nuke.selectedNode())
        os.startfile(os.path.normpath(os.path.dirname(nodeFilePath)))
    else:
        nukeFilePath=nuke.root().knob('name').value()
        os.startfile(os.path.normpath(os.path.dirname(nukeFilePath)))
tthunderToolbar.addCommand('Open File Directory', openFileDirectory, '^b',icon='%s/OpenFileDirectory.png' % tthToolbarIconsFolder)
tthunderToolbar.addSeparator()


# Add Presets
files = os.listdir(tthToolbarPresetsFolder)
files.sort()
for i in files:
    PresetsFullPath = tthToolbarPresetsFolder + '/' + i 
    if os.path.isfile(PresetsFullPath):
        FileName = os.path.splitext(i)[0]
        tthunderToolbar.addCommand(FileName, 'nuke.nodePaste(\"' + PresetsFullPath + '\")', icon='%s/%s.png'%(tthToolbarIconsFolder,FileName))


# Open Preset Directory
def openPresetDirectory():
    os.startfile(os.path.normpath(tthToolbarPresetsFolder))
tthunderToolbar.addCommand('Open Preset Directory', openPresetDirectory)