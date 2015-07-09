from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

try:
    import pypandoc
    long_description = pypandoc.convert(path.join(here, 'README.md'), 'rst')
except (IOError, ImportError):
    long_description = ''

setup(
    name='telezombie',

    version='0.2.1',

    description='Telegram Bot API with Tornado',
    long_description=long_description,

    url='https://github.com/legnaleurc/telezombie',

    author='Wei-Cheng Pan',
    author_email='legnaleurc@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Communications :: Chat',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='telegram bot tornado',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=['tornado >= 4'],

    extras_require={
        'dev': ['pypandoc'],
    },
)
