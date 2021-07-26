from setuptools import setup

setup(
        name='Descord2',
        packages=['descord'],
        version='0.2-25-g5b57a6e',
        description='Discord API wrapper for learning purpose.',
        author='thisgary',
        license='MIT',
        install_requires=['requests','websockets'],
        setup_requires=['pytest_runner'],
        test_require=['pytest'],
        test_suite='tests')

