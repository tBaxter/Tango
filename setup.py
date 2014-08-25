# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('docs/requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='django-tango',
    version='0.6.0',
    author=u'Tim Baxter',
    author_email='mail.baxter@gmail.com',
    description='Faster, simpler Django content management.',
    long_description=open('README.md').read(),
    url='https://github.com/tBaxter/Tango',
    license='LICENSE.txt',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    zip_safe=False,
)
