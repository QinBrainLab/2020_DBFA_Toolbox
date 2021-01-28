import os
import shutil

EnterPath = input("Please enter the path where anaconda3 you installed:(C;\\xxx\\xxx\\anaconda3):")
AnaPacPath = EnterPath + "\\Lib\\site-packages"
NowPath = os.getcwd()
PacPath = NowPath + "\\package"
DLLPath = EnterPath + "\\DLLs"
sqlite3Path = PacPath + "\\sqlite3.dll"
shutil.copy(sqlite3Path, DLLPath)
mplPath1 = AnaPacPath + "\\mpl_toolkits"
mplPath2 = PacPath + "\\mpl_toolkits"
shutil.copytree(mplPath1, mplPath2)
