"""
Setup script.
"""
import os
import sys
from setuptools import setup

version = '0.0.2'

if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'version v%s'" % (version, version))
    os.system("git push origin master --tags")
    sys.exit()

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()

if sys.argv[-1] == 'test':
    test_requirements = [
        'pytest',
    ]
    try:
        modules = map(__import__, test_requirements)
    except ImportError as e:
        err_msg = e.message.replace("No module named ", "")
        msg = "%s is not installed. Install your test requirments." % err_msg
        raise ImportError(msg)
    os.system('py.test')
    sys.exit()


try:
   import pypandoc
   long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    import io
    # pandoc is not installed, fallback to using raw contents
    with io.open('README.md', encoding="utf-8") as f:
        long_description = f.read()

setup(
    author='Ritesh Kadmawala',
    author_email='ritesh@loanzen.in',
    long_description=long_description,
    description='A simple falcon library that allows defining a single resource class to '
                'handle requests for a single item as well as multiple items',
    download_url='',
    setup_requires=['pytest-runner'],
    install_requires=[
        'falcon',
    ],
    license='MIT',
    name='falcon-resource-factory',
    packages=[
        'falcon_resource_factory',
    ],
    scripts=[],
    test_suite='tests',
    tests_require=[
        'pytest>=3.0.7,<4.0.0',
        'tox>=2.3.1,<3.0.0',
    ],
    url='https://github.com/loanzen/falcon-resource-factory',
    version=version
)
