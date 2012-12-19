# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '0.1'

setup(
    name='lethusbox',
    version=version,
    description="Uma coleção de feramentas para as aplicações da Lethus",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='django',
    author='Wilson Junior',
    author_email='wilsonpjunior@gmail.com',
    url='https://github.com/wpjunior/lethusbox',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
