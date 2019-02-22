from setuptools import setup, find_packages


setup(
    name='excavator',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click',
        'regex',
    ],
    extras_require={
        'dev': [
            'pytest',
        ],
    },
)
