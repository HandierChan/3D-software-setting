# 1.从选择的abc(会根据hip文件名的场景号"sc_*"进行筛选)文件中创建摄像机
# 2.匹配maya帧数
# 注意: maya2018导出abc至少要有一个关键帧(key帧)才能用 alembicTimeRange, 最后测试在houdini18

import hou
import _alembic_hom_extensions as abc

# HIP Scene Number, the theory is Three Digits. Example: SC001
hipName = hou.hipFile.basename()
hipName = hipName.split('.')[0]
if 'sc' in hipName:
    hipSC = [i for i in hipName.split('_') if 'sc'.lower() in i.lower()][0]
    if len(hipSC) is 3:
        hipSC = hipSC[:2] + '00' + hipSC[2:]
    if len(hipSC) is 4:
        hipSC = hipSC[:2] + '0' + hipSC[2:]
else: hipSC = ''

# Dialog for select file
abcFullFile = hou.ui.selectFile(pattern='*'+hipSC+'*'+'.abc', multiple_select=False)
abcFullFileAbs  = hou.expandString(abcFullFile)

# Set FrameRange
timeRange = abc.alembicTimeRange(abcFullFileAbs)
if timeRange is not None:
    hou.playbar.setFrameRange(hou.playbar.frameRange()[0], hou.timeToFrame(timeRange[1])-1)
    #hou.playbar.setPlaybackRange(hou.playbar.playbackRange()[0], hou.timeToFrame(timeRange[1])-1)

# Filter Camera, !!! Need Rewrite
abcMenuTuples = abc.alembicGetObjectPathListForMenu(abcFullFileAbs)
if abcMenuTuples is None: # report error when exiting the select abc dialog, so quit()
    quit()
cameraList=[]
for i in set(abcMenuTuples):
    cameraABCObject = abc.alembicGetSceneHierarchy(abcFullFileAbs,i)
    if cameraABCObject[1] == 'camera':
        cameraList.append(i)
cameraExclude = ['/front/frontshape','/top/topshape','/side/sideshape','/persp/perspshape','/left/leftshape','/right/rightshape','/back/backshape','/bottom/bottomshape']
cameraList=[i for i in cameraList if i.lower() not in cameraExclude]
cameraList=[i for i in cameraList if ':' not in i] # 冒号是 maya reference，过滤掉 reference 相机
if len(cameraList)==1:
    cameraName=cameraList[0]
else:
    userSelect = hou.ui.selectFromTree(cameraList, exclusive=1, title='Select Camera')
    try:cameraName=userSelect[0]
    except:quit()
cameraNameCorrect=cameraName.replace(':','_') # 冒号是 maya reference，会报错，其实上面 cameraList 已过滤 reference

######################## Create a series of camera nodes(Start)
obj = hou.node('/obj')
abcNull = obj.createNode('null')
abcNull.moveToGoodPosition()
abcNull.setParms({'scale':0.01})

abcArchive = abcNull.createOutputNode('alembicarchive')
abcArchive.setParms({'fileName':abcFullFile,'objectPath':cameraName})
abcArchive.parm('buildHierarchy').pressButton()

abcFetch = abcArchive.createOutputNode('fetch')
abcFetch.setParms({'useinputoffetched':1})
abcFetch.setParms({'fetchobjpath':abcArchive.path()+cameraNameCorrect})
abcFetch.setInput(0, None)

abcCamera = abcFetch.createOutputNode('cam')
abcCamera.setParms({'resx':1920,'resy':1080})
abcCamera.parm('focal').set(hou.node(abcArchive.path()+cameraNameCorrect).parm('focal'))
abcCamera.parm('aperture').set(hou.node(abcArchive.path()+cameraNameCorrect).parm('aperture'))
#abcCamera.parm('near').set(hou.node(abcArchive.path()+cameraNameCorrect).evalParm('near'))
#abcCamera.parm('far').set(hou.node(abcArchive.path()+cameraNameCorrect).evalParm('far'))

networkBox = obj.createNetworkBox()
networkBox.setComment('camera')
networkBox.addItem(abcNull)
networkBox.addItem(abcArchive)
networkBox.addItem(abcFetch)
networkBox.addItem(abcCamera)
networkBox.setSelected(1,1)
networkBox.fitAroundContents()

abcNull.setDisplayFlag(0)
abcNull.setSelectableInViewport(0)
abcArchive.setDisplayFlag(0)
abcArchive.setSelectableInViewport(0)
abcFetch.setDisplayFlag(0)
abcFetch.setSelectableInViewport(0)
abcCamera.setSelectableInViewport(0)
####################### Create a series of camera nodes(End)