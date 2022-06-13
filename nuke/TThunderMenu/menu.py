import os



# load this Folder Path
tthMenuCurrentFolder = os.path.dirname(__file__)
tthMenuIconsFolder = "%s/icons" % tthMenuCurrentFolder
tthMenuPresetsFolder = "%s/Presets" % tthMenuCurrentFolder
presetsNetworkFolder = "%s/Presets/Network" % tthMenuCurrentFolder


# Read Node Parameter
def unload_read():
    sels=nuke.selectedNodes()
    if len(sels):
        [i.knob('localizationPolicy').setValue("formAutoLocalizePath") for i in sels if 'localizationPolicy' in i.knobs()]
    else: 
        [i.knob('localizationPolicy').setValue("formAutoLocalizePath") for i in nuke.allNodes('Read') if 'localizationPolicy' in i.knobs()]
def load_read():
    sels=nuke.selectedNodes()
    if len(sels):
        [i.knob('localizationPolicy').setValue("on") for i in sels if 'localizationPolicy' in i.knobs()]
    else: 
        [i.knob('localizationPolicy').setValue("on") for i in nuke.allNodes() if 'localizationPolicy' in i.knobs()]
def reload_read():
    for i in nuke.allNodes():
        if 'updateLocalization' in i.knobs():
            i.knob('updateLocalization').execute()
        if 'reload' in i.knobs():
            i.knob('reload').execute()




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
                menuObject.addCommand(FileName, 'nuke.nodePaste(\'' + FileFullPath + '\')', icon='%s/%s.png'%(tthMenuIconsFolder,FileName))




#######################(Start) Build TTH Menu
TThunderMenu = nuke.menu('Nuke').addMenu('TTH')

Playback = nuke.menu('Nuke').addMenu('&TTH/Playback', icon='%s/Playback.png'%tthMenuIconsFolder)
Playback.addCommand('FirstFrame', lambda: nuke.activeViewer().frameControl(-6), '^Up')
Playback.addCommand('PreviousKeyframe', lambda: nuke.activeViewer().frameControl(-4), '^Left')
Playback.addCommand('Pause', lambda: nuke.activeViewer().frameControl(0), 'Down')
Playback.addCommand('Play', lambda: nuke.activeViewer().frameControl(5), 'Up')
Playback.addCommand('NextKeyframe', lambda: nuke.activeViewer().frameControl(4), '^Right')
Playback.addCommand('LastFrame', lambda: nuke.activeViewer().frameControl(6), '^Down')

TThunderMenu.addSeparator()
monitor = nuke.menu('Nuke').addMenu('&TTH/Performance Monitor', icon='%s/Monitor.png'%tthMenuIconsFolder)
monitor.addCommand('Start', lambda: nuke.startPerformanceTimers(), '', icon='')
monitor.addCommand('Stop', lambda: nuke.stopPerformanceTimers(), '', icon='')

TThunderMenu.addSeparator()
Localization = nuke.menu('Nuke').addMenu('&TTH/Localization', icon='%s/Localization.png'%tthMenuIconsFolder)
Localization.addCommand('Unload (Read Node)', unload_read, 'F9', icon='%s/Write.png'%tthMenuIconsFolder)
Localization.addCommand('Load (Read Node)', load_read, '+F9', icon='%s/Read.png'%tthMenuIconsFolder)
Localization.addCommand('Reload (Read Node)', reload_read, '^F9', icon='%s/DeepRecolor.png'%tthMenuIconsFolder)

TThunderMenu.addSeparator()
LockNodeMenu = nuke.menu('Nuke').addMenu('&TTH/Lock Node', icon='%s/MarkerRemoval.png'%tthMenuIconsFolder)
LockNodeMenu.addCommand('Lock', 'LockNode(True)', '')
LockNodeMenu.addCommand('Unlock', 'LockNode(False)', '')

TThunderMenu.addSeparator()
PresetsNetworkMenu = nuke.menu('Nuke').addMenu('&TTH/Presets/Network', icon='%s/NukeApp32.png'%tthMenuIconsFolder)
PresetsMenu = nuke.menu('Nuke').addMenu('&TTH/Presets', icon='%s/NukeApp32.png'%tthMenuIconsFolder)
CreatePresetsMenu(presetsNetworkFolder, PresetsNetworkMenu)
CreatePresetsMenu(tthMenuPresetsFolder, PresetsMenu)

# Open Preset Directory
def openPresetDirectory():
    os.startfile(os.path.normpath(tthMenuPresetsFolder))
PresetsMenu.addCommand('Open Preset Directory', openPresetDirectory)

#######################(End) Build TTH Menu



