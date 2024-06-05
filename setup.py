from setuptools import setup, find_packages

setup(
    name='dbt-x-looker',
    version='0.1.0',
    author='Mathias Nørskov',
    author_email='mathiasnoerskov@gmail.com',
    description='A dbt and looker integration toolbox',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mathiasDK/dbt-x-looker',  # replace with your repo URL
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    install_requires=[
        # List your project's dependencies here, e.g.,
        # 'numpy>=1.18.5',
    ],
    tests_require=[
        'unittest',
    ],
    test_suite='unittest',
)
