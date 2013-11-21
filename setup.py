from setuptools import setup

setup(
    name='scenariobuilder',
    version='0.1.8',
    packages=['scenariobuilder'],
    license='Apache',
    url='https://github.com/CiscoSystems/scenariobuilder',
    install_requires=['python-novaclient', 'python-neutronclient', 'PyYaml', 'Jinja2'],
    scripts=['bin/sb'],
    include_package_data=True
)


