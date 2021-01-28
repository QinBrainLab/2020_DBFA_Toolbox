# Developmental Brain Functional Activity (DBFA) maps

**Attention: Please unzip ‘package’ before installation.**

‘AnaDir’ is the path where you installed Anaconda3. 
‘DBFADir’ is the path where the DevelopmentalBrainFunctionalActivityMaps folder locates. 

Note: For users who do not want to install this toolbox, you can directly navigate to ‘DBFADir’\map and find the maps you want. 

Win10 64bit version of operating system is recommended. Python 3.7 are required with the Anaconda on the official website. After the installation, please add the path of ‘AnaDir’\Anaconda3 and ‘AnaDir’\Anaconda3\Scripts to the system environment variables. 

Open Anaconda Powershell Prompt and execute the following code in order: 
cd ‘DBFADir’\package
pip uninstall -r Pkg_Uninstall.txt
pip install -r Pkg_Install.txt (If ‘ERROR: spyder ……’ occurs, just ignore)

cd ‘AnaDir’\Scripts
python cxfreeze-postinstall

cd ‘DBFADir’
python Setting1.py
python Setup.py build
python Setting2.py

Double click DBFA.exe that in ‘DBFADir’\build\exe.win-amd64-3.7 to run. 

Once installed, the build folder can be removed or renamed. To release space, you can also remove DevelopmentalBrainFunctionalActivityMaps folder in your computer. It may take a long time to get ready for the first time, please be patient. 
