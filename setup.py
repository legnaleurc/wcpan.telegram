import os.path as op

from setuptools import setup


with open(op.join(op.dirname(__file__), './README.rst')) as fin:
    long_description = fin.read()


setup(
    name='wcpan.telegram',

    version='0.3.0.dev5',

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
        'Programming Language :: Python :: 3.5',
    ],

    keywords='telegram bot tornado',

    packages=[
        'wcpan.telegram',
    ],

    install_requires=['tornado >= 4'],
)
