# https://gist.github.com/zhuzhuor/7250173#gistcomment-3861063

import sys
try:
    import py2exe
except:
    input('Please install py2exe first...')
    sys.exit(-1)

from distutils.core import setup
import shutil

sys.argv.append('py2exe')

setup(
    options={
        'py2exe': {'bundle_files': 1, 'compressed': True}
    },
    console=[
        {'script': "hello.py"}
    ],
    zipfile=None,
)

shutil.move('dist\\hello.exe', '.\\hello.exe')
# shutil.rmtree('build')
shutil.rmtree('dist')
