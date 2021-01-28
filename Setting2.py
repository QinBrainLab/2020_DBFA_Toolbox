import os
import shutil

NowPath = os.getcwd()
PacPath = NowPath + "\\package"
FBAlibPath = NowPath + "\\build\\exe.win-amd64-3.7\\lib"
mplPath1 = PacPath + "\\mpl_toolkits"
mplPath2 = FBAlibPath + "\\mpl_toolkits"
shutil.copytree(mplPath1, mplPath2)
mulPath1 = FBAlibPath + "\\multiprocessing\\Pool.pyc"
mulPath2 = FBAlibPath + "\\multiprocessing\\pool.pyc"
shutil.move(mulPath1, mulPath2)
patsyPath1 = FBAlibPath + "\\patsy\\Origin.pyc"
patsyPath2 = FBAlibPath + "\\patsy\\origin.pyc"
shutil.move(patsyPath1, patsyPath2)
FBAPath = NowPath + "\\build\\exe.win-amd64-3.7"
pngPath = NowPath + "\\begin.png"
icoPath = NowPath + "\\python.ico"
shutil.copy(pngPath, FBAPath)
shutil.copy(icoPath, FBAPath)
mapPath1 = NowPath + "\\map"
mapPath2 = FBAPath + "\\map"
shutil.copytree(mapPath1, mapPath2)
shutil.rmtree(mplPath1)