from setuptools import setup
from pip.req import parse_requirements

REQS = [str(ir.req) for ir in parse_requirements('requirements.txt')]

setup(
    name='tabletopscanner',
    packages=['tabletopscanner'],
    include_package_data=True,
    install_requires=REQS,
)