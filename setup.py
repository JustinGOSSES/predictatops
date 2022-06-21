#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup_requirements = ['click',
'matplotlib',
'folium',
'bokeh',
'branca',
'welly',
'lasio',
'scikit-learn',
'numpy',
'numba',
'pooch',
'scipy',
'tables',
'xgboost']

"""The setup script."""
requirements  = ['Click>=6.0',
'bokeh==0.13.0',
'branca==0.3.0',
'certifi==2018.4.16',
'chardet==3.0.4',
'click==6.7',
'cloudpickle==0.5.3',
'cryptography',
'Cython==0.28.3',
'cytoolz==0.9.0.1',
'dask==0.18.2',
'dask-glm==0.1.0',
'dask-ml==0.7.0',
'dask-xgboost==0.1.5',
'decorator==4.3.0',
'distributed==1.22.0',
'folium==0.5.0',
'lasio==0.21',
'matplotlib==2.2.2',
'mkl-random==1.0.1',
'numba==0.39.0',
'numpy==1.22.0',
'pandas==0.23.3',
'pickleshare==0.7.4',
'pooch==0.3.1',
'requests>=2.20.0',
'scikit-learn==0.19.1',
'scipy==1.1.0',
'seaborn==0.9.0',
'striplog==0.7.3',
'tables==3.4.4',
'urllib3>=1.24.2',
'welly==0.3.5',
'xgboost==0.72.1',
'dask==0.18.2',
'dask-glm==0.1.0',
'dask-ml==0.7.0',
'dask-xgboost==0.1.5',
'decorator==4.3.0',
'distributed==1.22.0',
'entrypoints==0.2.3',
'ipykernel==4.8.2',
'ipython==6.4.0',
'ipython-genutils==0.2.0',
'ipywidgets==7.2.1',
'isort==4.3.15',
'jupyter==1.0.0',
'jupyter-client==5.2.3',
'jupyter-console==5.2.0',
'jupyter-core==4.4.0',
]


test_requirements = ['pytest','pytest-runner']

setup(
    author="Justin Gosses",
    author_email='jgosses82@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="A series of modules for various steps involved in a stratigraphic pick machine-learning prediction project",
    entry_points={
        'console_scripts': [
            'predictatops=predictatops.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='predictatops',
    name='predictatops',
    packages=find_packages(include=['predictatops']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/JustinGOSSES/predictatops',
    version='0.1.0',
    zip_safe=False,
)
