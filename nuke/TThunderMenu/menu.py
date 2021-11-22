import os

import KnobDefaults


# load this Folder Path
CurrentFolder = os.path.dirname(__file__)
IconsFolder = "%s/icons" % CurrentFolder
PresetsFolder = "%s/Presets" % CurrentFolder
PresetsNetworkFolder = "%s/Presets/Network" % CurrentFolder


# Read Node Parameter
def unload_read():
    sels=nuke.selectedNodes()
    if len(sels):
        [i.knob('localizationPolicy').setValue("formAutoLocalizePath") for i in sels]
    else: 
        [i.knob('localizationPolicy').setValue("formAutoLocalizePath") for i in nuke.allNodes('Read')]
def load_read():
    sels=nuke.selectedNodes()
    if len(sels):
        [i.knob('localizationPolicy').setValue("on") for i in sels]
    else: 
        [i.knob('localizationPolicy').setValue("on") for i in nuke.allNodes('Read')]
def reload_read():
    for n in nuke.allNodes('Read'):
        n.knob('updateLocalization').execute()
        n.knob('reload').execute()



# Lock Node
def LockNodeAddLabel(node):
    labelValue = node['label'].getValue().strip('\n')
    labelCheck = labelValue.split()
    if len(labelCheck) == 0:
        node['label'].setValue('___Node_Locked___')
    elif '___Node_Locked___' not in labelCheck[-1]:
        node['label'].setValue(labelValue + '\n___Node_Locked___')
def LockNodeRemoveLabel(node):
    labelValue = node['label'].getValue()
    labelCheck = labelValue.split('\n')
    if len(labelCheck) != 0:
        if '___Node_Locked___' in labelCheck[-1]:
            labelCheck = labelCheck[:-1]
    labelJoin = '\n'.join(labelCheck)
    node['label'].setValue(labelJoin)
def LockNode(state):
    nodes = nuke.selectedNodes()
    for node in nodes:
        allknobs = node.allKnobs()
        for knob in allknobs:
            knob.setEnabled(not state)
        if state:
            LockNodeAddLabel(node)
        if not state:
            LockNodeRemoveLabel(node)



# Load "Presets" folder in this File Path
def CreatePresetsMenu(origPath, menuObject):
    files = os.listdir(origPath)
    files.sort()
    for file in files:    
        FileFullPath = origPath + '/' + file 
        #if os.path.isdir(FileFullPath):
        #    tmpMenu = menuObject.addMenu(file)
        #    CreatePresetsMenu((FileFullPath + '/'), tmpMenu)
        if os.path.isfile(FileFullPath):
            if (os.path.splitext(FileFullPath)[1] == '.nk'):
                FileName = os.path.splitext(file)[0]
                menuObject.addCommand(FileName, 'nuke.nodePaste(\'' + FileFullPath + '\')', icon='%s/%s.png'%(IconsFolder,FileName))


'''
# Build Toolbar Menu, "Reveal In Explorer"
def RevealInExplorer():
    node = nuke.selectedNode()
    if node.knob("file") is not None:
    #if node.Class()=="Read" or node.Class()=="Write":
        fullpath = node['file'].value()
        path = os.path.split(fullpath)[0]
        path = os.path.normpath(path)
        cmd = 'explorer "%s"' % path
        os.system(cmd)
RevealMenu=nuke.toolbar('Nodes')
RevealMenu.addCommand('Reveal In Explorer', RevealInExplorer, icon='%s/FileExplorer.png' % IconsFolder)
'''


#######################(Start) Build TTH Menu
TThunderMenu = nuke.menu('Nuke').addMenu('TTH')

Playback = nuke.menu('Nuke').addMenu('&TTH/Playback', icon='%s/Playback.png'%IconsFolder)
Playback.addCommand('FirstFrame', lambda: nuke.activeViewer().frameControl(-6), '^Up')
Playback.addCommand('PreviousKeyframe', lambda: nuke.activeViewer().frameControl(-4), '^Left')
Playback.addCommand('Pause', lambda: nuke.activeViewer().frameControl(0), 'Down')
Playback.addCommand('Play', lambda: nuke.activeViewer().frameControl(5), 'Up')
Playback.addCommand('NextKeyframe', lambda: nuke.activeViewer().frameControl(4), '^Right')
Playback.addCommand('LastFrame', lambda: nuke.activeViewer().frameControl(6), '^Down')

TThunderMenu.addSeparator()
monitor = nuke.menu('Nuke').addMenu('&TTH/Performance Monitor', icon='%s/Monitor.png'%IconsFolder)
monitor.addCommand('Start', lambda: nuke.startPerformanceTimers(), '', icon='')
monitor.addCommand('Stop', lambda: nuke.stopPerformanceTimers(), '', icon='')

TThunderMenu.addSeparator()
Localization = nuke.menu('Nuke').addMenu('&TTH/Localization', icon='%s/Localization.png'%IconsFolder)
Localization.addCommand('Unload (Read Node)', unload_read, 'F9', icon='%s/Write.png'%IconsFolder)
Localization.addCommand('Load (Read Node)', load_read, '+F9', icon='%s/Read.png'%IconsFolder)
Localization.addCommand('Reload (Read Node)', reload_read, '^F9', icon='%s/DeepRecolor.png'%IconsFolder)

TThunderMenu.addSeparator()
LockNodeMenu = nuke.menu('Nuke').addMenu('&TTH/Lock Node', icon='%s/MarkerRemoval.png'%IconsFolder)
LockNodeMenu.addCommand('Lock', 'LockNode(True)', '')
LockNodeMenu.addCommand('Unlock', 'LockNode(False)', '')

TThunderMenu.addSeparator()
PresetsMenu = nuke.menu('Nuke').addMenu('&TTH/Presets', icon='%s/NukeApp32.png'%IconsFolder)
PresetsNetworkMenu = nuke.menu('Nuke').addMenu('&TTH/Presets/Network', icon='%s/NukeApp32.png'%IconsFolder)
CreatePresetsMenu(PresetsNetworkFolder, PresetsNetworkMenu)
CreatePresetsMenu(PresetsFolder, PresetsMenu)


#######################(End) Build TTH Menu



