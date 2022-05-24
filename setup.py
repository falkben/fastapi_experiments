from setuptools import find_packages, setup

with open("requirements.in") as f:
    requirements = f.read().splitlines()

setup(name="experiments", packages=find_packages(), install_requires=requirements)
