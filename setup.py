from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='telezombie',

    version='0.1',

    description='Telegram Bot API with Tornado',
    long_description=long_description,

    url='https://github.com/legnaleurc/telezombie',

    author='Wei-Cheng Pan',
    author_email='legnaleurc@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Communications :: Chat',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='telegram tornado',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=['tornado >= 4', 'pyyaml'],
)
