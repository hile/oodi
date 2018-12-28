
from setuptools import setup, find_packages
from oodi import __version__

setup(
    name='oodi',
    keywords='music library tagging transcoding management soundforest',
    description='python tools to manage music libraries and files',
    author='Ilkka Tuohela',
    author_email='hile@iki.fi',
    url='https://github.com/hile/oodi/',
    version=__version__,
    license='PSF',
    packages=find_packages(),
    python_requires='>3.6.0',
    entry_points={
        'console_scripts': [
            'oodi=oodi.bin.oodi:main',
        ],
    },
    install_requires=(
        'mutagen',
        'ruamel.yaml',
        'multiprocessing',
        'systematic',
    ),
    tests_require=(
        'pytest',
        'pytest-runner',
        'pytest-datafiles',
    ),
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Topic :: System',
        'Topic :: System :: Systems Administration',
    ],
)
