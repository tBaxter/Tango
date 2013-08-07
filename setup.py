# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='django-tango',
    version='0.1',
    description='Faster, simpler Django content management.',
    long_description=open('README.md').read(),
    url='https://github.com/tBaxter/Tango',
    license='BSD license, see LICENSE.txt',
    author=u'Tim Baxter',
    author_email='mail.baxter@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    #zip_safe=False,
    dependency_links = ['http://github.com/tBaxter/django-voting/tarball/master#egg=django-voting-0.1']
)
