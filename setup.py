# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages
from setuptools.command.develop import develop
from subprocess import check_call
from os import path


class update_submodules(develop):
    def run(self):
        print 1
        if path.exists('.git'):
            check_call(['git', 'submodule', 'update', '--init', '--recursive'])
        develop.run(self)

a = setup(
    cmdclass = {"develop": update_submodules},
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
)
