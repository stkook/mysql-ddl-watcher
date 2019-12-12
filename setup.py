try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__author__ = 'ST <stkook@gmail.com>'
__version__ = '1.0.0'

packages = ['mysql_ddl_watcher']

package_dir = {
    'mysql_ddl_watcher': "src/"
}

install_requires = [
    "pymysql",
    "requests",
    "jsondiff",
]

setup(
    name='mysql-ddl-watcher',
    version=__version__,
    author='ST',
    author_email='stkook@gmail.com',
    license='MIT',
    url='https://github.com/stkook/mysql-ddl-watcher/tree/master',
    install_requires=install_requires,
    test_requires=[],
    keywords='MySQL DDL Watcher',
    description='Detect changing MySQL DDL statement and notification changed information',
    packages=packages,
    package_dir=package_dir,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.6',
    ]
)