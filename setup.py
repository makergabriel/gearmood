import os
import sys
import setuptools
from setuptools import find_packages, setup


base_dir = os.path.dirname(__file__)
src_dir = os.path.join(base_dir, "src")

# When executing the setup.py, we need to be able to import ourselves, this
# means that we need to add the src/ directory to the sys.path.
sys.path.insert(0, src_dir)

PACKAGES = find_packages(where="src")

setup(
    name='GearMood',
    version='0.1',
    packages=PACKAGES,
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read()
)