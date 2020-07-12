import os
import codecs
from setuptools import setup, find_packages


version = '0.2.dev2'


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


install_requires = [
    'Django>=1.11,<4.0',
    'django-widget-tweaks>=1.4,<=1.5'
]


test_requires = [
]


setup(
    name='django-spectre-css',
    version=version,
    description='Spectre CSS for Django',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author='Nils Rokita',
    author_email='0rokita@informatik.uni-hamburg.de',
    maintainer='Nils Rokita',
    maintainer_email='0rokita@informatik.uni-hamburg.de',
    url='https://github.com/fsinfuhh/django-spectre-css',
    license='License :: OSI Approved :: MIT License',
    packages=find_packages(),
    install_requires=install_requires,
    package_data={
        "": ["static/css/lib/*.css", "templates/spectre-css/*.html"],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Framework :: Django',
    ]
)
