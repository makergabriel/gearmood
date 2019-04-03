import os
import sys
import setuptools
from setuptools import find_packages, setup


BASE_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(BASE_DIR, "src")

# When executing the setup.py, we need to be able to import ourselves, this
# means that we need to add the src/ directory to the sys.path.
sys.path.insert(0, SRC_DIR)

PACKAGES = find_packages(where="src")

setup(
    name='GearMood',
    version='0.1',
    packages=PACKAGES,
    package_dir={"": "src"},
    package_data={'src': ['config/*',]},
    include_package_data=True,
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read()
)