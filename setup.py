
from setuptools import setup, find_packages

setup(
    name = 'ngin',
    version = '0.1',
    license='MIT',
    description = 'ngin',
    author = 'Hoewon Kim',
    author_email="hoewon.im@gmail.com",
    packages = ['ngin'],
    url='https://github.com/danielhwkim/ngin-py3',
    install_requires=[
            'zeroconf',
            'protobuf',
        ],
)
