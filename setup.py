#from distutils.core import setup
# from distutils.extension import Extension
from setuptools import find_packages, setup, Extension
import os
try:
    from Cython.Build import cythonize
    USE_CYTHON = True
except ModuleNotFoundError:
    USE_CYTHON = False

ext = '.pyx' if USE_CYTHON else '.c'

extensions = [Extension("radbsdf", ["src/radbsdf"+ext])]

if USE_CYTHON:
    if not os.path.isdir("Radiance"):
        raise ModuleNotFoundError("Radiance module not found")

    rad_common = os.path.join("Radiance", "src", "common")

    bsdf_files = os.path.join(rad_common, "BSDFfiles.txt")

    if not os.path.isfile(bsdf_files):
        raise FileNotFoundError(bsdf_files + " not found")

    with open(bsdf_files) as rdr:
        bsdf_file_list = rdr.read().strip().splitlines()

    bsdf_source_files = [os.path.join(rad_common, file) for file in bsdf_file_list
                         if file.endswith('.c')]

    source_files = ["src/radbsdf.pyx"] + bsdf_source_files

    extensions = [Extension(name="radbsdf", sources=source_files, language='c',)]

    extensions = cythonize(extensions)

setup(
     name='radbsdf',
     version='0.0.2',
     author='LBNL',
     author_email='taoningwang@lbl.gov',
     packages=find_packages(),
     ext_modules=extensions,
     zip_safe=False,
)
