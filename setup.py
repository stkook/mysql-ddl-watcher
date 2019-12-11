try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__author__ = 'ST <stkook@gmail.com>'
__version__ = '1.0.0'

packages = [
    'src',
]

setup(
    name='mysql-ddl-watcher',
    version=__version__,
    author='ST',
    author_email='stkook@gmail.com',
    license='MIT',
    url='https://github.com/stkook/mysql-ddl-watcher/tree/master',
    install_requires=[],
    test_requires=[],
    keywords='MySQL DDL Watcher',
    description='Detect changing MySQL DDL statement and notification changed information',
    packages=packages,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.5',
    ]
)