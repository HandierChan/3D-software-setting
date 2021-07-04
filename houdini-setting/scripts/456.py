'''
文件复制到 %HOMEPATH%\Documents\houdini17.0\scripts\456.py
或在 houdini.env 文件里加入 "HOUDINI_PATH = 路径"，会自动读取路径里的 scripts\456.py
'''

import hou
import os


hou.setFps(25)
hou.appendSessionModuleSource('''hou.hscript("autosave off")''')


def SetProjectPath():
    '''
    从 $HIPFILE 路径后面往前，搜到带 "houdini" 就设置此路径为 $JOB
    '''
    filePath = hou.hipFile.path()
    filePath = filePath.split('/')
    for i in range(len(filePath)):
        if 'houdini' in filePath[-1].lower():
            break
        filePath.pop()
    prjPath = '/'.join(filePath)
    hou.putenv('JOB', prjPath)
    print('$' + 'JOB = ' + hou.getenv('JOB', 'None'))
SetProjectPath()


def Install_HDA(path, hdaFolderWhiteLists=['hda','otls'], hdaFolderBlacklists=['old','olds','backup','history'], hdaExtension=['.hda','.otl']):
    '''
    递归每个文件夹，自动加载搜索到的 HDA
    path: 要搜索的路径
    hdaFolderWhiteLists: 搜索路径里，只寻找这些文件夹
    hdaFolderBlacklists: 搜索路径里，不寻找这些文件夹
    hdaExtension: 只搜索这些后缀名的文件（减少搜索时间）
    '''
    for hdaFolder in hdaFolderWhiteLists:
        hdaFullPath = path.replace('\\','/') + '/' + hdaFolder
        for hdaRoot, hdaDirs, hdaFiles in os.walk(hdaFullPath, topdown=True):
            hdaDirs[:] = [i for i in hdaDirs if i not in hdaFolderBlacklists]
            for hdaFile in hdaFiles:
                for ext in hdaExtension:
                    if os.path.splitext(hdaFile)[1] == ext:
                        # print(os.path.normpath(path))
                        hou.hda.installFile(os.path.join(hdaRoot, hdaFile))
Install_HDA(hou.getenv('JOB','None'), ['hda','hip/FX','hip/lighting']) # $JOB自身
Install_HDA(r'\\data2\wangpan\install\houdini') # tthunder库目录
Install_HDA(r'\\data2\E\QQH_TV_S01\media1\HoudiniProject') # 旗旗号第一季
Install_HDA(r'\\data4\E\QQH_TV_S02\QQH_TV_S02_0Library\Houdini_Project') # 旗旗号第二季
