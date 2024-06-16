from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='SimpleEDA',
    version='0.1.0',
    description='A simple library for exploratory data analysis',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/kitranet/SimpleEDA',  # Replace with your project's URL
    author='M.R.Vijay Krishnan',
    author_email='vijaykrishnanmr@gmail.com',
    packages=find_packages(),
    install_requires=[
        'seaborn',
        'matplotlib',
        'numpy',
        'pandas',
        'statsmodels'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='EDA data-analysis',
    python_requires='>=3.6',
)