from setuptools import find_packages, setup

setup(
        name='Descord2',
        packages=find_packages(include=['descord',]),
        version='0.2-17-gcf3826c',
        description='Discord API Python wrapper for learning purposes.',
        author='thisgary',
        license='MIT',
        install_requires=['requests'],
        setup_requires=['pytest_runner'],
        test_require=['pytest'],
        test_suite='tests')

