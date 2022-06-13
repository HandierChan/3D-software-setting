#encoding:utf-8

'''
1.自动把当前TTH目录的所有mel和py文件，加载到maya主菜单"TTH"
2.需要代码能自动执行，如默认SubmitMayaToDeadline.mel没有自动执行，需要最后加"SubmitJobToDeadline();"
3.mel加载用eval('source path')，python加载用execfile(path)
4."../../icons" 自动加载图标路径，文件名跟代码一一对应，只能用png
5.TTH菜单只有单列表，后期文件多再加上子菜单功能
'''

import maya.cmds as cmds
import maya.mel as mel
from pymel.core import Callback
import os

def pyFileMayaExecute(fullPath='z:/aa.py'):
    path=os.path.normpath(fullPath)
    execfile(path)

def melFileMayaExecute(fullPath='z:/aa.mel'):
    path=os.path.normpath(fullPath)
    path=path.replace("\\","/")
    mel.eval(r'source "%s"'%path)

def createMenuTTH():
    menuObject='TTH'
    if cmds.menu(menuObject,exists=1,parent='MayaWindow'):
        cmds.deleteUI(cmds.menu(menuObject,edit=1,deleteAllItems=1))
    cmds.menu(menuObject,tearOff=True,parent='MayaWindow')

def fileFilter(extension=['.py','.mel']):
    # tthPath="C:/Users/tthunder/Documents/maya/2018/scripts/tth"
    tthPath=os.path.dirname(__file__)
    fileList = os.listdir(tthPath)

    # Remove list element: [__file__.py,__init__.py] and so on
    baseName=os.path.basename(__file__)
    for i in fileList:
        if os.path.splitext(baseName)[0] in os.path.splitext(i)[0]:
            fileList.remove(i)
    removeList=['__init__.py']
    for i in removeList:
        if i in fileList:
            fileList.remove(i)

    fileExtFilterList=[]
    for i in fileList:
        if os.path.splitext(i)[1] in extension:
            fileExtFilterList.append(i)

    pyFullPathList=[os.path.normpath(tthPath+'/'+i) for i in fileExtFilterList]
    return pyFullPathList

def addMenuItem_mel(fileList_mel):
    cmds.menuItem(label='MEL',divider=True)
    for i in fileList_mel:
        iName=os.path.splitext(os.path.basename(i))[0]
        cmds.menuItem(label=iName,c=Callback(melFileMayaExecute,i),image=iName+'.png')

def addMenuItem_py(fileList_py):
    cmds.menuItem(label='Python',divider=True)
    for i in fileList_py:
        iName=os.path.splitext(os.path.basename(i))[0]
        cmds.menuItem(label=iName,c=Callback(pyFileMayaExecute,i),image=iName+'.png')

def openMaDirectory():
    filePath=cmds.file(q=True,sn=True)
    fileDir=os.path.dirname(filePath)
    os.startfile(fileDir)
def openFileDirectory():
    '''
    open select node directory:
    maya file,texture node,redshift proxy and vdb,
    '''
    parmList=['fileTextureName','fileName']
    parmListLen=len(parmList)
    parmListCount=0

    selectNodeList=cmds.ls(selection=True)
    if selectNodeList==[]:
        openMaDirectory()
        import sys
        sys.exit()

    selectNode=selectNodeList[0]
    for i in parmList:
        try:
            texturePath=cmds.getAttr(selectNode+'.'+i)
            if texturePath:
                textureDir=os.path.dirname(texturePath)
                os.startfile(textureDir)
                break
        except:pass

        parmListCount+=1
        if parmListCount==parmListLen:
            openMaDirectory()

def openScriptDirectory():
    tthPath=os.path.dirname(__file__)
    cmds.menuItem(label='Open Script Directory',c=lambda x:os.startfile(tthPath))

def main():
    createMenuTTH()
    
    cmds.menuItem(label='Open File Directory',c=lambda x:openFileDirectory(),image='Open File Directory.png')

    # script preset (mel and py)
    fileList=fileFilter(['.py','.mel'])
    melList,pyList=[],[]
    [melList.append(i) for i in fileList if os.path.splitext(i)[1]=='.mel']
    [pyList.append(i) for i in fileList if os.path.splitext(i)[1]=='.py']
    if melList: addMenuItem_mel(melList)
    if pyList: addMenuItem_py(pyList)

    cmds.menuItem(divider=True)
    openScriptDirectory()