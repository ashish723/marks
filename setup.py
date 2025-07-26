from setuptools import setup, find_packages,setup
from typing import List

def get_requirements(file_path:str)->list[str]:
    """ this function returns the list of requirements"""


setup(
author='Ashish verma',
email='ashish42v@gmail.com',
name='marksproject',
version='0.0.1',
packages=find_packages(),
# install_packages=get_requirements('requirements.txt')
)