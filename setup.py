#!/usr/bin/env python3
"""
Python setuptools script for ``yubu_goog`` tool.
"""
from yubigoog import __version__
from setuptools import setup

setup(
    name='yubigoog',
    version=__version__,
    description='Generate TOTP tokens from Yubikeys, automatically type them.',
    long_description=(
        "Calculates TOTP tokens from HOTP responses of Yubikeys, includes a "
        "setup process and emulated keyboard strokes for typing out the token "
        "so you can use it with a keyboard shortcut."
    ),
    author='Greenhost BV',
    author_email='info@greenhost.nl',
    url='https://github.com/greenhost/yubi-goog',
    python_requires='>=2.7, >=3.5.*, <4',
    packages=['yubigoog'],
    install_requires=[
        'PyAutoGUI>=0.9.41',
        'python3-xlib>=0.15',
        'keyboard>=0.13.2',
        'python-yubico>=1.3.3',
    ],
    license='MIT',
    classifiers=[
        'Development Status :: ',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Security',
        'Topic :: Utilities',
    ],
    keywords='yubikey GoogleAuthenticator totp hotp hid',
    entry_points={
        'console_scripts': [
            'yubigoog = yubigoog.__main__:main'
        ]
    }
)
