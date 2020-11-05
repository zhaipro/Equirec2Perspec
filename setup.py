from distutils.core import setup, Extension


setup(name='sample', ext_modules=[Extension('equirec2perspec', ['wrapper.cpp'])])
