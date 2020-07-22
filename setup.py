from setuptools import setup

setup(name='spg',
    version='0.0.1',
    description='simple webapp that serves images videos from a folder (and subfolders)',
    url='https://github.com/ChristianS99/spg',
    author='https://github.com/ChristianS99',
    license='MIT',
    packages=['spg'],
    package_data={'spg': [ 'templates/*.jinja2', ],},
    scripts = [
        'bin/spg'
    ],
    install_requires = [
        'aiohttp',
        'aiohttp_jinja2',
        'python-magic',
    ]
)