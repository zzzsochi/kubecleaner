from setuptools import setup

VERSION = '0.0'


setup(
    name='kubecleaner',
    version=VERSION,
    description="Clean trash from you kubernetes",
    author='Alexander "ZZZ" Zelenyak',
    author_email='zzz.sochi@gmail.com',
    platforms='any',
    install_requires=['docopt', 'kubernetes'],
    packages=['kubecleaner'],
)
