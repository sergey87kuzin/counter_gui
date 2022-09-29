from setuptools import setup

APP_NAME = 'Stock'
APP = ['stock_counter.py']
DATA_FILES = [('db', ['db/gui.db'])]
# APP_NAME = 'GuiApp'
# APP = ['app.py']
# DATA_FILES = []
OPTIONS = {
    # 'packages': ['colour', 'contourpy', 'cycler', 'mccabe',
    #              'kiwisolver', 'macholib',
    #              'modulegraph', 'numpy', 'packaging',
    #              'PIL', 'pyparsing', 'pages', 'six'],
    'iconfile': 'icon_for_counter.icns',
    'matplotlib_backends': '*',
    # 'argv_emulation': True,
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': 'Desktop Founds Control',
        'CFBundleVersion': '0.1'
    }
}

setup(
    app=APP,
    name=APP_NAME,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
