# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

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
    #zip_safe=False,
    #dependency_links = ['https://github.com/tBaxter/capo.git']
)
