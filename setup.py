import os.path

from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import setup, find_packages


def extract_requirements(filename):
    return [str(r.req) for r in parse_requirements(filename, session=PipSession())]


# load metadata
base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, 'README.rst')) as f:
    long_description = f.read()

install_requires = extract_requirements('requirements.txt')

setup(
    name='build_docker_env',
    version='0.0.1-dev',
    packages=find_packages(),
    url='',
    license='Proprietary',
    author='Josha Inglis',
    author_email='josha.inglis@biarri.com',
    description='Helper to generate a Docker development environment',
    install_requires=install_requires,
    scripts=['bin/build_env'],
    entry_points="""\
    [console_scripts]
    build_env = env_builder.cli:build_env
    """
)
