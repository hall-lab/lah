# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('lah/version.py') as f:
    exec(f.read())

tests_require = [
    "mock",
    "nose",
]
install_requires=[
    "biopython>=1.46",
    "click==7.0",
    "Jinja2>=2.10.1",
    "natsort",
    "pyyaml==5.1",
    "SQLAlchemy>=1.3.10",
    "tabulate",
    "yoyo-migrations>=6.1.0",
]

setup(
    name='lah',
    version=__version__,
    description='Sequence Transform',
    long_description=readme,
    author='Eddie Belter',
    author_email='ebelter@wustl.edu',
    license=license,
    url='https://github.com/hall-lab/lah.git',
    install_requires=install_requires,
    entry_points='''
        [console_scripts]
        lah=lah.cli:cli
    ''',
    setup_requires=["pytest-runner"],
    test_suite="nose.collector",
    tests_requires=tests_require,
    packages=find_packages(include=['lah'], exclude=('tests')),
    include_package_data=True,
    package_data={"lah": ["db-migrations/*"]},
)
