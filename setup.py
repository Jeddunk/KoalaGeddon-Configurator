from setuptools import setup

setup(
    name='Koala-GUI',
    version='1.0',
    packages=[#Point to main.py and to the logos folder#],
    install_requires=[
    "ttkthemes~=3.2.2",
    "Pillow~=8.1.2"
    ],
    url='https://github.com/g-yui',
    license='GNU GPLv3',
    author='yui',
    author_email='',
    description='KG-GUI'
)
