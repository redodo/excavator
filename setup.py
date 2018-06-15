from setuptools import setup, find_packages


setup(
    name='dirtcastle',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'apistar',
        'click',
        'pymongo',
        'regex',
        'falcon',
    ],
    entry_points='''
        [console_scripts]
        dirtcastle=dirtcastle.api.cli:cli
    '''
)
