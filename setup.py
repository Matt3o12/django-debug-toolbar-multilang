from setuptools import setup
import sys

extra_install_requires = []
if sys.version_info < (3, 3):
    extra_install_requires.append("mock")

def get_long_description():
    with open('README.md', "rt") as file:
        return file.read()

setup(
    name='django-debug-toolbar-multilang',
    version='1.0',
    description='Language panel for django-debug-toolbar',
    long_description=get_long_description(),
    url='http://github.com/matt3o12/django-debug-toolbar-multilang',
    author='Matteo Kloiber',
    author_email='info@matt3o12.de',
    license='MIT',
    packages=["debug_toolbar_multilang"],
    install_requires = ["Django>=1.7.1", "django-debug-toolbar"] + extra_install_requires,
)