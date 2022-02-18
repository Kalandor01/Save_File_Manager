from setuptools import setup, find_packages

from save_file_manager import __version__

setup(
    name='save_file_manager',
    version=__version__,

    url='https://github.com/Kalandor01/save_file_manager',
    author='Kalandor01',
    author_email='rohovszkyakoska@gmail.com',

    packages=find_packages(),
    
    install_requires=[
        'base64',
        'numpy',
    ],
)
