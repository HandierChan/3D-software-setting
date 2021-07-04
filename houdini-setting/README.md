# 存放路径
文件夹对应放在 `%HOMEPATH%\Documents\houdini18.0\`

# 文件说明
## MainMenuCommon.xml
1. 效果：菜单栏加上"TTH"
2. 目的：导出Alembic文件
3. 关联文件 ./scripts/CreateCameraFromABCAuto.py 和 ./scripts/CreateCameraFromABCSelect.py

## scripts/123.py
1. 目的：设置帧率为25

## scripts/456.py
1. A目的：自动设置工程目录，从 $HIPFILE 路径后面往前，搜到带 "houdini" 就设置此路径为 $JOB；</br>
B目的：用文件夹分类很多个 hda ，但 houdini 环境变量(houdini.env)只能一个个文件夹加载，于是写下这个代码，自动递归加载文件夹里每个 hda 文件
2. 如何使用：主要是修改 Install_HDA() 里面内容，可多次增加
3. 代码示意说明：
```
# 默认搜索 hdapath 里面 hda、otls 文件夹的 hda 文件；
hdapath = 'C:/Users/handier/Documents/houdini18.0'
Install_HDA(hdapath)
```
```
# D:/houdini18.0` 里有三个文件夹，会搜索 aa、bb 文件夹，而不会搜索 cc 文件夹
mypath = 'D:/houdini18.0'
Install_HDA(mypath,['aa','bb'],['cc'])
```
