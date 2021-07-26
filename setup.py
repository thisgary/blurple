from setuptools import setup

setup(
        name='Descord2',
        packages=['descord'],
        version='0.2-24-g7b32daf',
        description='Discord API Python wrapper for learning purposes.',
        author='thisgary',
        license='MIT',
        install_requires=['requests'],
        setup_requires=['pytest_runner'],
        test_require=['pytest'],
        test_suite='tests')

