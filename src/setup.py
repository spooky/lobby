# -*- coding: utf-8 -*-
# Run the build process by running the command 'python setup.py build'

import sys
import os
from cx_Freeze import setup, Executable

base = None
include_files = []

if sys.platform == 'win32':
    base = 'Win32GUI'
    import PyQt5
    PYQT5_DIR = os.path.dirname(PyQt5.__file__)
    LUA_DIR = os.path.normpath('D:/tools/LuaJIT')  # TODO: bad bad bad
    include_files = [
        'ui',
        (os.path.join(PYQT5_DIR, 'qml', 'QtQuick.2'), 'QtQuick.2'),
        (os.path.join(PYQT5_DIR, 'qml', 'QtQuick'), 'QtQuick'),
        (os.path.join(PYQT5_DIR, 'qml', 'QtGraphicalEffects'), 'QtGraphicalEffects'),
        (os.path.join(PYQT5_DIR, 'qml', 'Qt'), os.path.join('Qt')),
        (LUA_DIR, '.'),
    ]
# need linux stuff here

options = {
    'build_exe': {
        'include_files': include_files,
        'includes': [
            # 'atexit', 'sip', 'asyncio', 'lupa', 'aiohttp', 'ws4py',
            # 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets',
            # 'PyQt5.QtNetwork', 'PyQt5.QtOpenGL', 'PyQt5.QtQml', 'PyQt5.QtQuick',
            'view_models.games'  # TODO: bad bad bad, want full packages here e.g: 'games'
        ],
        'excludes': ['Tkinter'],
        'optimize': 2,
        'compressed': True,
        'include_msvcr': True
    }
}

executables = [
    Executable('main.py', base=base, targetName='FAForever.exe', icon='ui/icons/faf.ico')
]

setup(
    name='faforever',
    version='0.1.0',
    description='Forged Aliance Forever lobby',
    options=options,
    executables=executables
)
