import os
import logging

from distutils.command.install import INSTALL_SCHEMES
from distutils.core import setup


for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']


packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('thumbnails'):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]

    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])


setup(
    name='zero-thumbnails',
    version='0.1',
    description='App to add and manage thumbnails into a model',
    author='Jose Maria Zambrana Arze',
    author_email='contact@josezambrana.com',
    url='http://github.com/mandlaweb/zero-thumbnails',
    packages=packages,
    data_files=data_files,
    install_requires=['zero-common-app', 'Django>=1.3.1', 'South>=0.7.3', 
                      'PIL>=1.1.7']
)
