import setuptools

setuptools.setup(
        name='blurple',
        version='0.9',
        author='thisgary',
        author_email='gary.github@gmail.com',
        description='Yet another Discord API wrapper.',
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        packages=setuptools.find_packages(),
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT Lisence',
            'Operating System :: OS Independent',
        ],
        license='MIT',
        python_requires='>=3.8',
        install_requires=['requests', 'websockets'],
        setup_requires=['pytest_runner'],
        tests_require=['pytest'],
        test_suite='tests',
)

