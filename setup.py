from setuptools import setup

setup(
    name='scenariobuilder',
    version='0.1.3',
    packages=['scenariobuilder'],
    license='Apache',
    url='https://github.com/michaeltchapman/scenariobuilder',
    install_requires=['python-novaclient', 'python-neutronclient', 'PyYaml', 'Jinja2'],
    scripts=['bin/sb']
)


