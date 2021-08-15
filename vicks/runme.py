def run():
    import os
    # import shutil

    # os.system('pip install pyinstaller')
    os.system('pyinstaller --onefile hello.txt')

    # shutil.move('dist/hello.exe', 'uploads/py2exe/hello.exe')
    # shutil.rmtree('build')
    # shutil.rmtree('dist')
    # shutil.rmtree('__pycache__')

    # if os.path.exists("hello.spec"):
    #   os.remove("hello.spec")
