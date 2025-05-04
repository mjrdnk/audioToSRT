import sys
sys.setrecursionlimit(5000)

from setuptools import setup

APP = ['audio_to_srt.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'packages': ['whisper', 'torch', 'numpy', 'tkinter'],
    'includes': ['tkinter'],
    'iconfile': 'icon.icns',
    'plist': {
        'CFBundleName': 'Audio to SRT',
        'CFBundleDisplayName': 'Audio to SRT',
        'CFBundleGetInfoString': "Convert audio to SRT subtitles",
        'CFBundleIdentifier': "com.audiotosrt.app",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': "© 2025"
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
