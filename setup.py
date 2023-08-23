from setuptools import setup, find_packages


# Read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    description = f.read()

setup(
    name='pdb-toolkit',
    version='0.3.4',
    packages=find_packages(),
    url='https://github.com/raoufkeskes/pdb_toolkit',
    license='MIT Licence',
    author='raouf-ks',
    author_email='raouf.keskes@mabsilico.com',
    description=description,
    python_requires='>=3.6',
    install_requires=['wget'],
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"
        ],
)

