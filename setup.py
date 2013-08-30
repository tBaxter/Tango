# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('docs/requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='django-tango',
    version='0.3',
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
    dependency_links = [
        'http://github.com/tBaxter/tango-shared-core/tarball/master#egg=tango-shared-0.5',
        'http://github.com/tBaxter/tango-articles/tarball/master#egg=tango-articles-0.3',
        'http://github.com/tBaxter/tango-contact-manager/tarball/master#egg=tango-contact-0.4',
        'http://github.com/tBaxter/django-voting/tarball/master#egg=tango-voting-0.1'
    ]
)
