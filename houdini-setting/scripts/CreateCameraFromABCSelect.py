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

# Set FrameRange
timeRange = abc.alembicTimeRange( hou.expandString(abcFullFile))
if timeRange is not None:
    hou.playbar.setFrameRange(hou.playbar.frameRange()[0], hou.timeToFrame(timeRange[1])-1)
    #hou.playbar.setPlaybackRange(hou.playbar.playbackRange()[0], hou.timeToFrame(timeRange[1])-1)

# Filter Camera, (Need Optimization!!!)
abcMenuTuples = abc.alembicGetObjectPathListForMenu( hou.expandString(abcFullFile))
if abcMenuTuples is None:
    quit()
cameraList=[]
for i in set(abcMenuTuples):
    cameraABCObject = abc.alembicGetSceneHierarchy(abcFullFile, i)
    if cameraABCObject[1] == 'camera':
        cameraList.append(i)
cameraExclude = ['/front/frontShape','/top/topShape','/side/sideShape','/persp/perspShape']
cameraList=[i for i in cameraList if i not in cameraExclude]
cameraList=[i for i in cameraList if ':' not in i]
if len(cameraList)==1:
    cameraName=cameraList[0]
else:
    userSelect = hou.ui.selectFromTree(cameraList, exclusive=1, title='Select Camera')
    try:cameraName=userSelect[0]
    except:quit()
cameraNameCorrect=cameraName.replace(':','_') # 纠正maya-reference名字，上面cameraList已过滤reference

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