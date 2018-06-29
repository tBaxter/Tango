# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('docs/requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='django-tango',
    version='0.9.2',
    author=u'Tim Baxter',
    author_email='mail.baxter@gmail.com',
    url='https://github.com/tBaxter/Tango',
    license='MIT',
    description='Faster, simpler Django content management.',
    long_description=open('README.md').read(),
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
)
