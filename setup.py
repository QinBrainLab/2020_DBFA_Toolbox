import sys
#import os
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('BrainAtlas_PyQt5.py', targetName='FBA.exe', base=base,icon='python.ico')
]

include_files = []

buildOptions = dict(
    packages=['sklearn', 'nibabel', 'scipy', 'numpy', 'matplotlib', 'tkinter', 'pandas', 'patsy'],
    excludes=["scipy.spatial.cKDTree"],
    include_files=include_files,
)

setup(
    name='FBA',
    version='1.2',
    description='',
    options=dict(build_exe=buildOptions),
    executables=executables
)
