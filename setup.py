from os import path

from setuptools import setup, find_packages


with open(op.join(op.dirname(__file__), './README.rst')) as fin:
    long_description = fin.read()


setup(
    name='wcpan.telegram',

    version='0.3.0.dev1',

    description='Telegram Bot API with Tornado',
    long_description=long_description,

    url='https://github.com/legnaleurc/wcpan.telegram',

    author='Wei-Cheng Pan',
    author_email='legnaleurc@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Communications :: Chat',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='telegram bot tornado',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=['tornado >= 4'],
)
