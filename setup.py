#-*- coding: utf-8 -*-
import os
import sys
from subprocess import Popen, PIPE
from setuptools import setup, Extension


def opencv_pkg_config(kind):
    process_pkg_config = Popen(['pkg-config', 'opencv', kind], stdout=PIPE)
    return process_pkg_config.communicate()[0].strip().split(' ')


DIR_FERNS_DEMO = "ferns_demo-1.1"
tmp_opencv_libs = opencv_pkg_config('--libs')
opencv_includes = opencv_pkg_config('--cflags')

opencv_libs = []
for lib in tmp_opencv_libs:
    if lib.startswith('-l'):
        opencv_libs.append(lib[2:])
    else:
        opencv_libs.append(lib)

sys.path.append('./src')

version = file('VERSION').read().strip()

# get sources
sources = ['_ferns.i', 'planar_pattern_detector_wrapper.cpp']
for tpl in os.walk(DIR_FERNS_DEMO):
    for filename in tpl[2]:
        for ext in ('.cc',):
            if ext in filename and 'main' not in filename:
                sources.append(os.path.join(tpl[0], filename))

ferns_ext = Extension('_ferns',
                      include_dirs=[DIR_FERNS_DEMO] + map(lambda i: i[2:], opencv_includes),
                      sources=sources,
                      libraries=opencv_libs,
                      swig_opts=['-c++'],
                      )

setup(name='pyferns',
      version=version,
      description="Python wrapper for Fern-based planar patch detector demonstration in EPFL (in development)",
      long_description=file(DIR_FERNS_DEMO + '/README').read(),
      classifiers=[],
      keywords=('image processing'),
      author='Takahiro Kamatani',
      author_email='tk@buhii.org',
      url='https://github.com/buhii/pyferns',
      license='LGPL',
      package_dir={'': 'src'},
      packages=['pyferns'],
      ext_modules=[ferns_ext],
      #install_requires=["cv"],
      #test_suite='test_ccv.suite'
      )
