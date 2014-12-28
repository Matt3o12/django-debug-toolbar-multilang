from setuptools import setup
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
    version='1.0',
    description='Language panel for django-debug-toolbar',
    long_description=get_long_description(),
    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='README.md',
    url='http://github.com/matt3o12/django-debug-toolbar-multilang',
    author='Matteo Kloiber',
    author_email='info@matt3o12.de',
    license='MIT',
    packages=["debug_toolbar_multilang"],
    install_requires=requirements
)