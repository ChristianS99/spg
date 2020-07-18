from setuptools import setup

setup(name='spg',
    version='0.0.1',
    description='simple webapp that serves images videos from a folder (and subfolders)',
    #url='http://github.com/storborg/funniest',
    #author='Flying Circus',
    #author_email='flyingcircus@example.com',
    #license='MIT',
    packages=['spg'],
    scripts = [
        'bin/spg'
    ],
    #zip_safe=False,
    install_requires = [
        'aiohttp',
        'aiohttp_jinja2',
        'python-magic',
    ]
)