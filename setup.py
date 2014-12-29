from setuptools import setup, find_packages
import sys


def get_long_description():
    with open('README.rst', "rt") as file:
        return file.read()

requirements = []
if sys.version_info < (3, 3):
    requirements.append("mock")

requirements.append("Django>=1.7.1")
requirements.append("django-debug-toolbar")

setup(
    name='django-debug-toolbar-multilang',
    version='1.0.1',
    description='Language panel for django-debug-toolbar',
    long_description=get_long_description(),
    url='http://github.com/matt3o12/django-debug-toolbar-multilang',
    author='Matteo Kloiber',
    author_email='info@matt3o12.de',
    license='MIT',
    include_package_data=True,
    packages=find_packages(exclude=('tests.*', 'tests')),
    install_requires=requirements,
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Natural Language :: German",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",

    ],
    zip_safe=False
)