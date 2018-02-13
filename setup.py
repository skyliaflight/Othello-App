from distutils.core import setup
import py2exe
setup(options = {'py2exe': {'bundle_files': 2, 'compressed': True}},
      zipfile = None,
      windows=['cartesian.py', 'game_classes.py', 'othello_interface.py'])