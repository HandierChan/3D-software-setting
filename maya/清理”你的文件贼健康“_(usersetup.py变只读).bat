:: userSetup.py会变只读，安装某些插件要注意

c:
cd /d "%HOMEPATH%\Documents\maya\scripts"

:: 允许权限修改
::icacls userSetup.py /grant  %USERNAME%:(f)
icacls vaccine.py /grant  %USERNAME%:(f)
::attrib -r userSetup.py
attrib -r vaccine.py

:: 替换userSetup.py, 防止误删
type userSetup.py | findstr /v vaccine | findstr /v leukocyte >> userSetup_temp.py
type userSetup_temp.py > userSetup.py
del /f userSetup_temp.py

del /f vaccine.py
del /f vaccine.pyc
type nul > vaccine.py

:: icacls userSetup.py /deny %USERNAME%:(w)
:: 加只读
attrib +r userSetup.py
attrib +r vaccine.py