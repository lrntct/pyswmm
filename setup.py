# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""Python setup.py installer script."""

# Standard library imports
import ast
import os
import sys

# Third party imports
from setuptools import find_packages, setup
from setuptools.extension import Extension
from setuptools.command.build_ext import build_ext

HERE = os.path.abspath(os.path.dirname(__file__))
PY2 = sys.version_info.major == 2


def get_version(module='pyswmm'):
    """Get version."""
    with open(os.path.join(HERE, module, '__init__.py'), 'r') as f:
        data = f.read()
    lines = data.split('\n')
    for line in lines:
        if line.startswith('VERSION_INFO'):
            version_tuple = ast.literal_eval(line.split('=')[-1].strip())
            version = '.'.join(map(str, version_tuple))
            break
    return version


def get_description():
    """Get long description."""
    with open(os.path.join(HERE, 'README.rst'), 'r') as f:
        data = f.read()
    return data


# get a list of SWMM source files
SWMM_SOURCE = os.path.join('pyswmm', 'owaswmm', 'src')
SWMM_INCLUDES = [SWMM_SOURCE, os.path.join('pyswmm', 'owaswmm', 'include')]

def swmm_get_source():
    """locate and return a list of source files
    """
    file_list = []
    for f in os.listdir(SWMM_SOURCE):
        if f.endswith('.c'):
            file_list.append(os.path.join(SWMM_SOURCE,f))
    return file_list


# compiler CLI arguments
copt =  {'msvc': ['/openmp', '/Ox'],
         'mingw32' : ['-O3', '-w', '-fopenmp', '-lgomp', '-lpthread'],
         'unix' : ['-O3', '-w', '-fopenmp']
         }
lopt =  {'mingw32' : ['-lgomp', '-lpthread'],
         'unix' : ['-lgomp']
         }


class build_ext_compiler_check(build_ext):
    def build_extensions(self):
        compiler = self.compiler.compiler_type
        print("compiler: {}".format(compiler))
        if compiler in copt:
           for e in self.extensions:
               e.extra_compile_args = copt[compiler]
        if compiler in lopt:
            for e in self.extensions:
                e.extra_link_args = lopt[compiler]
        build_ext.build_extensions(self)


# swmm build
ext_swmm = Extension('pyswmm.lib.swmm5', sources=swmm_get_source(),
                     include_dirs=SWMM_INCLUDES)

REQUIREMENTS = ['six']

if sys.version_info < (3, 4):
    REQUIREMENTS.append('enum34')

setup(
    name='pyswmm',
    version=get_version(),
    description='Python Wrapper for SWMM5 API',
    long_description=get_description(),
    url='https://github.com/OpenWaterAnalytics/pyswmm/wiki',
    author='Bryant E. McDonnell (EmNet LLC)',
    author_email='bemcdonnell@gmail.com',
    install_requires=REQUIREMENTS,
    ext_modules=[ext_swmm],
    cmdclass={'build_ext': build_ext_compiler_check},
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    package_data={
        '': ['swmm/lib/*',
            'LICENSE.txt', 'AUTHORS', 'tests/data/*.inp', 'tests/*.py'
        ]
    },
    include_package_data=True,
    license="BSD2 License",
    keywords="swmm5, swmm, hydraulics, hydrology, modeling, collection system",
    classifiers=[
        "Topic :: Scientific/Engineering",
        "Topic :: Documentation :: Sphinx",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: C",
        "Development Status :: 4 - Beta",
    ])
