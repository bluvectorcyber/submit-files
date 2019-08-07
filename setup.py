# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import os.path

PKG_NAME = 'submit_to_bv'

def get_install_requirements(path):
    with open(path, 'r') as reqs:
        return [req for req in reqs.readlines() if req not in ('', '#')]

# Grab version string form __init__.py to avoid import that may break
# instalation if dependent packages imported by this pkg are not yet installed
def get_version(pkg_name):
    init = os.path.join(os.path.dirname(__file__), pkg_name, '__init__.py')
    version_line = list(filter( lambda l: l.startswith('__version__'), open(init)))[0]
    return eval(version_line.split('=')[-1])

setup(
    name=PKG_NAME.replace('_', '-'),
    version=get_version(PKG_NAME),
    author="BluVector",
    author_email="info@bluvector.io",
    url="https://www.bluvector.io",
    description="Package suited to submit files/directories to the BluVector Portal and log the results",
    license="Apache 2.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'submit-files=submit_to_bv.submit_to_bv:main',
        ]
    },
    install_requires=get_install_requirements("requirements.txt")
)
