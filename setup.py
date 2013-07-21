# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-tango',
    version='0.1',
    author=u'Tim Baxter',
    author_email='mail.baxter@gmail.com',
    packages=find_packages(),
    url='https://github.com/tBaxter/Tango',
    license='BSD licence, see LICENCE.txt',
    description='Faster, simpler Django content management.',
    long_description=open('README.md').read(),
    include_package_data=True,
    zip_safe=False,
    dependency_links = ['https://github.com/tBaxter/capo.git']
)
