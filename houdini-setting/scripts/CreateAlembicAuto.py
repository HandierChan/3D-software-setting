# Auto search ABC File based on HIP File

import os,hou
import _alembic_hom_extensions as abc

def KeywordtoSearchFileName(keyword,searchPath,isfile,raiseError=1):
    fileLists = os.listdir(searchPath)
    if isfile:
        result = [i for i in fileLists if os.path.isifle(searchPath+'/'+i) and keyword.lower() in i.lower()]
    else:
        result = [i for i in fileLists if os.path.isdir(searchPath+'/'+i) and keyword.lower() in i.lower()]
    if len(result) is 1:
        return result[0]
    elif raiseError is 1:
        hou.ui.displayMessage('Error: Unclear \"'+ keyword +'\" Keyword, need to modify Python Script.',title='Search Path',severity=hou.severityType.Error)

# Search ABC Path (Output by Maya). Example: //data2/E/QQH_TV_S01/media1_e01/Maya_Project/scenes/Render/abc
if len(hou.getenv('JOB','')) is 0:
    hou.ui.displayMessage('Error: $JOB is None',severity=hou.severityType.Error)
else:
    jobPath = hou.getenv('JOB').split('/')
episodePath = '/'.join( jobPath[0:-1])
mayaSearch = KeywordtoSearchFileName('maya', episodePath, 0, 1)
mayaPath = episodePath + '/' + mayaSearch
sceneSearch = KeywordtoSearchFileName('scenes', mayaPath, 0, 1)
scenePath = mayaPath + '/' + sceneSearch
renderSearch = KeywordtoSearchFileName('render', scenePath, 0, 1)
renderPath = scenePath + '/' + renderSearch
abcSearch = KeywordtoSearchFileName('abc', renderPath, 0, 1)
abcPath = renderPath + '/' + abcSearch
# Search ABC File. Example: QQH_EP03_SC001_Anim_V01_out1_frm124.abc
abcLists = os.listdir(abcPath)
abcLists = [i for i in abcLists if os.path.splitext(i)[1] == '.abc']
abcLists = [i for i in abcLists if len(i.split("_")) > 5]

# Match to ABC File from hip scene Number. Example: SC001 ==> QQH_EP03_SC001_Anim_V01_out1_frm124.abc
hipName = hou.hipFile.basename()
hipSC = [i for i in hipName.split('_') if 'sc'.lower() in i.lower()][0]
if len(hipSC) is 3:
    hipSC = hipSC[:2] + '00' + hipSC[2:]
if len(hipSC) is 4:
    hipSC = hipSC[:2] + '0' + hipSC[2:]
for i in range(len(abcLists)-1, -1, -1):
    if abcLists[i].split('_')[2] != hipSC:
        del abcLists[i]
abcLists.sort()
abcFile = abcLists[-1]
abcFullFile = abcPath+'/'+abcFile

######################## Create nodes(Start)
obj = hou.node('/obj')
abcGeo = obj.createNode('geo','alembic1')
abcGeo.setSelected(1,1)
abcGeo.moveToGoodPosition()
for i in abcGeo.children():
    i.destroy()
abcArchive = abcGeo.createNode('alembic','alembic1')
abcArchive.setParms({'fileName':abcFullFile, 'groupnames':4, 'curveFilter':0})

abctransform = abcArchive.createOutputNode('xform')
abctransform.setParms({'scale':.01})
abctransform.setDisplayFlag(1)
abctransform.setRenderFlag(1) 
####################### Create nodes(End)